import torch
import torch.nn as nn
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import DataLoader
from torch.utils.data.distributed import DistributedSampler
import torch.multiprocessing as mp
import os
import time
import logging
from typing import Dict, Any, Optional, Tuple, List
import numpy as np
from datetime import datetime
import json
import pickle

from ..models.compatibility_network import CompatibilityNeuralNetwork
from ..models.transformer import CompatibilityTransformer
from ..data.compatibility_dataset import CompatibilityDataset

class DistributedCompatibilityTrainer:
    """
    Distributed trainer for neural compatibility models using PyTorch DDP
    Supports multi-GPU and multi-node training with automatic mixed precision
    """
    
    def __init__(self, config: Dict[str, Any], rank: int = 0, world_size: int = 1):
        self.config = config
        self.rank = rank
        self.world_size = world_size
        self.device = torch.device(f'cuda:{rank}' if torch.cuda.is_available() else 'cpu')
        
        # Initialize distributed training
        if world_size > 1:
            self._setup_distributed()
        
        # Setup logging
        self._setup_logging()
        
        # Initialize model, optimizer, and scheduler
        self.model = self._create_model()
        self.optimizer = self._create_optimizer()
        self.scheduler = self._create_scheduler()
        self.criterion = self._create_loss_function()
        
        # Mixed precision training
        self.scaler = torch.cuda.amp.GradScaler() if config.get('use_amp', True) else None
        
        # Training state
        self.current_epoch = 0
        self.global_step = 0
        self.best_loss = float('inf')
        self.best_accuracy = 0.0
        
        # Metrics tracking
        self.train_metrics = []
        self.val_metrics = []
        
    def _setup_distributed(self):
        """Initialize distributed training environment"""
        os.environ['MASTER_ADDR'] = self.config.get('master_addr', 'localhost')
        os.environ['MASTER_PORT'] = str(self.config.get('master_port', 12355))
        
        # Initialize process group
        dist.init_process_group(
            backend='nccl',
            rank=self.rank,
            world_size=self.world_size
        )
        
        # Set device for this process
        torch.cuda.set_device(self.rank)
        
    def _setup_logging(self):
        """Setup logging for distributed training"""
        log_level = logging.INFO if self.rank == 0 else logging.WARNING
        
        logging.basicConfig(
            level=log_level,
            format=f'[Rank {self.rank}] %(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'training_rank_{self.rank}.log'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        
    def _create_model(self) -> nn.Module:
        """Create and initialize the neural compatibility model"""
        model_config = self.config['model']
        model_type = model_config.get('type', 'compatibility_network')
        
        if model_type == 'compatibility_network':
            model = CompatibilityNeuralNetwork(
                embedding_dim=model_config.get('embedding_dim', 512),
                num_dimensions=model_config.get('num_dimensions', 12)
            )
        elif model_type == 'compatibility_transformer':
            model = CompatibilityTransformer(
                embed_dim=model_config.get('embed_dim', 512),
                num_layers=model_config.get('num_layers', 6),
                num_heads=model_config.get('num_heads', 8)
            )
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        # Move model to device
        model = model.to(self.device)
        
        # Wrap with DDP if using distributed training
        if self.world_size > 1:
            model = DDP(model, device_ids=[self.rank], output_device=self.rank)
        
        return model
    
    def _create_optimizer(self) -> torch.optim.Optimizer:
        """Create optimizer with proper parameter groups"""
        opt_config = self.config['optimizer']
        
        # Parameter groups for different learning rates
        transformer_params = []
        cnn_params = []
        other_params = []
        
        for name, param in self.model.named_parameters():
            if 'transformer' in name:
                transformer_params.append(param)
            elif 'conv' in name:
                cnn_params.append(param)
            else:
                other_params.append(param)
        
        param_groups = [
            {'params': transformer_params, 'lr': opt_config.get('transformer_lr', 1e-4)},
            {'params': cnn_params, 'lr': opt_config.get('cnn_lr', 2e-4)},
            {'params': other_params, 'lr': opt_config.get('base_lr', 1e-4)}
        ]
        
        optimizer_type = opt_config.get('type', 'adamw')
        
        if optimizer_type == 'adamw':
            optimizer = torch.optim.AdamW(
                param_groups,
                weight_decay=opt_config.get('weight_decay', 1e-5),
                betas=opt_config.get('betas', (0.9, 0.999)),
                eps=opt_config.get('eps', 1e-8)
            )
        elif optimizer_type == 'adam':
            optimizer = torch.optim.Adam(param_groups)
        elif optimizer_type == 'sgd':
            optimizer = torch.optim.SGD(
                param_groups,
                momentum=opt_config.get('momentum', 0.9),
                weight_decay=opt_config.get('weight_decay', 1e-5)
            )
        else:
            raise ValueError(f"Unknown optimizer type: {optimizer_type}")
        
        return optimizer
    
    def _create_scheduler(self) -> Optional[torch.optim.lr_scheduler._LRScheduler]:
        """Create learning rate scheduler"""
        scheduler_config = self.config.get('scheduler', {})
        scheduler_type = scheduler_config.get('type', 'cosine_annealing')
        
        if not scheduler_type:
            return None
        
        if scheduler_type == 'cosine_annealing':
            scheduler = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(
                self.optimizer,
                T_0=scheduler_config.get('T_0', 10),
                T_mult=scheduler_config.get('T_mult', 2),
                eta_min=scheduler_config.get('eta_min', 1e-6)
            )
        elif scheduler_type == 'reduce_on_plateau':
            scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
                self.optimizer,
                mode='min',
                factor=scheduler_config.get('factor', 0.5),
                patience=scheduler_config.get('patience', 10),
                min_lr=scheduler_config.get('min_lr', 1e-6)
            )
        elif scheduler_type == 'step_lr':
            scheduler = torch.optim.lr_scheduler.StepLR(
                self.optimizer,
                step_size=scheduler_config.get('step_size', 30),
                gamma=scheduler_config.get('gamma', 0.1)
            )
        else:
            self.logger.warning(f"Unknown scheduler type: {scheduler_type}")
            return None
        
        return scheduler
    
    def _create_loss_function(self) -> nn.Module:
        """Create loss function for compatibility prediction"""
        loss_config = self.config.get('loss', {})
        loss_type = loss_config.get('type', 'mse')
        
        if loss_type == 'mse':
            criterion = nn.MSELoss()
        elif loss_type == 'mae':
            criterion = nn.L1Loss()
        elif loss_type == 'huber':
            criterion = nn.HuberLoss(delta=loss_config.get('delta', 1.0))
        elif loss_type == 'compatibility_loss':
            criterion = CompatibilityLoss(
                alpha=loss_config.get('alpha', 1.0),
                beta=loss_config.get('beta', 0.5)
            )
        else:
            raise ValueError(f"Unknown loss type: {loss_type}")
        
        return criterion
    
    def train_epoch(self, train_loader: DataLoader, epoch: int) -> Dict[str, float]:
        """Train for one epoch"""
        self.model.train()
        
        total_loss = 0.0
        total_accuracy = 0.0
        total_samples = 0
        
        start_time = time.time()
        
        for batch_idx, batch in enumerate(train_loader):
            # Move batch to device
            batch = {k: v.to(self.device) if torch.is_tensor(v) else v for k, v in batch.items()}
            
            # Forward pass with mixed precision
            with torch.cuda.amp.autocast(enabled=self.scaler is not None):
                if isinstance(self.model, DDP):
                    outputs = self.model.module.forward(**batch)
                else:
                    outputs = self.model(**batch)
                
                # Calculate loss
                if isinstance(outputs, dict):
                    predictions = outputs['compatibility_scores']
                else:
                    predictions = outputs
                
                loss = self.criterion(predictions, batch['targets'])
            
            # Backward pass
            self.optimizer.zero_grad()
            
            if self.scaler is not None:
                self.scaler.scale(loss).backward()
                self.scaler.unscale_(self.optimizer)
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
                self.scaler.step(self.optimizer)
                self.scaler.update()
            else:
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
                self.optimizer.step()
            
            # Update metrics
            batch_size = batch['targets'].size(0)
            total_loss += loss.item() * batch_size
            total_samples += batch_size
            
            # Calculate accuracy (for compatibility scores)
            with torch.no_grad():
                accuracy = self._calculate_accuracy(predictions, batch['targets'])
                total_accuracy += accuracy * batch_size
            
            # Log progress
            if batch_idx % self.config.get('log_interval', 100) == 0 and self.rank == 0:
                elapsed_time = time.time() - start_time
                samples_per_sec = total_samples / elapsed_time
                
                self.logger.info(
                    f'Epoch: {epoch}, Batch: {batch_idx:>6d}, '
                    f'Loss: {loss.item():.6f}, '
                    f'Accuracy: {accuracy:.4f}, '
                    f'Samples/sec: {samples_per_sec:.1f}'
                )
            
            self.global_step += 1
        
        # Calculate epoch metrics
        avg_loss = total_loss / total_samples
        avg_accuracy = total_accuracy / total_samples
        
        # Synchronize metrics across processes
        if self.world_size > 1:
            loss_tensor = torch.tensor([avg_loss], device=self.device)
            accuracy_tensor = torch.tensor([avg_accuracy], device=self.device)
            
            dist.all_reduce(loss_tensor, op=dist.ReduceOp.AVG)
            dist.all_reduce(accuracy_tensor, op=dist.ReduceOp.AVG)
            
            avg_loss = loss_tensor.item()
            avg_accuracy = accuracy_tensor.item()
        
        return {
            'train_loss': avg_loss,
            'train_accuracy': avg_accuracy,
            'learning_rate': self.optimizer.param_groups[0]['lr']
        }
    
    def validate_epoch(self, val_loader: DataLoader, epoch: int) -> Dict[str, float]:
        """Validate for one epoch"""
        self.model.eval()
        
        total_loss = 0.0
        total_accuracy = 0.0
        total_samples = 0
        
        with torch.no_grad():
            for batch in val_loader:
                # Move batch to device
                batch = {k: v.to(self.device) if torch.is_tensor(v) else v for k, v in batch.items()}
                
                # Forward pass
                if isinstance(self.model, DDP):
                    outputs = self.model.module.forward(**batch)
                else:
                    outputs = self.model(**batch)
                
                # Calculate loss
                if isinstance(outputs, dict):
                    predictions = outputs['compatibility_scores']
                else:
                    predictions = outputs
                
                loss = self.criterion(predictions, batch['targets'])
                
                # Update metrics
                batch_size = batch['targets'].size(0)
                total_loss += loss.item() * batch_size
                total_samples += batch_size
                
                # Calculate accuracy
                accuracy = self._calculate_accuracy(predictions, batch['targets'])
                total_accuracy += accuracy * batch_size
        
        # Calculate metrics
        avg_loss = total_loss / total_samples
        avg_accuracy = total_accuracy / total_samples
        
        # Synchronize metrics across processes
        if self.world_size > 1:
            loss_tensor = torch.tensor([avg_loss], device=self.device)
            accuracy_tensor = torch.tensor([avg_accuracy], device=self.device)
            
            dist.all_reduce(loss_tensor, op=dist.ReduceOp.AVG)
            dist.all_reduce(accuracy_tensor, op=dist.ReduceOp.AVG)
            
            avg_loss = loss_tensor.item()
            avg_accuracy = accuracy_tensor.item()
        
        return {
            'val_loss': avg_loss,
            'val_accuracy': avg_accuracy
        }
    
    def _calculate_accuracy(self, predictions: torch.Tensor, targets: torch.Tensor) -> float:
        """Calculate compatibility prediction accuracy"""
        # For regression, consider predictions within 10% of target as accurate
        tolerance = 0.1
        correct = torch.abs(predictions - targets) <= tolerance
        accuracy = correct.float().mean().item()
        return accuracy
    
    def train(self, train_dataset: CompatibilityDataset, val_dataset: CompatibilityDataset):
        """Main training loop"""
        # Create data loaders
        train_sampler = DistributedSampler(train_dataset) if self.world_size > 1 else None
        val_sampler = DistributedSampler(val_dataset) if self.world_size > 1 else None
        
        train_loader = DataLoader(
            train_dataset,
            batch_size=self.config['batch_size'],
            shuffle=(train_sampler is None),
            sampler=train_sampler,
            num_workers=self.config.get('num_workers', 4),
            pin_memory=True,
            drop_last=True
        )
        
        val_loader = DataLoader(
            val_dataset,
            batch_size=self.config['batch_size'],
            shuffle=False,
            sampler=val_sampler,
            num_workers=self.config.get('num_workers', 4),
            pin_memory=True
        )
        
        # Training loop
        num_epochs = self.config['num_epochs']
        
        for epoch in range(self.current_epoch, num_epochs):
            # Set epoch for samplers
            if train_sampler is not None:
                train_sampler.set_epoch(epoch)
            if val_sampler is not None:
                val_sampler.set_epoch(epoch)
            
            # Train epoch
            train_metrics = self.train_epoch(train_loader, epoch)
            
            # Validate epoch
            val_metrics = self.validate_epoch(val_loader, epoch)
            
            # Update scheduler
            if self.scheduler is not None:
                if isinstance(self.scheduler, torch.optim.lr_scheduler.ReduceLROnPlateau):
                    self.scheduler.step(val_metrics['val_loss'])
                else:
                    self.scheduler.step()
            
            # Combine metrics
            epoch_metrics = {**train_metrics, **val_metrics, 'epoch': epoch}
            
            # Save metrics
            self.train_metrics.append(epoch_metrics)
            
            # Log epoch results
            if self.rank == 0:
                self.logger.info(
                    f'Epoch {epoch:>3d}: '
                    f'Train Loss: {train_metrics["train_loss"]:.6f}, '
                    f'Val Loss: {val_metrics["val_loss"]:.6f}, '
                    f'Train Acc: {train_metrics["train_accuracy"]:.4f}, '
                    f'Val Acc: {val_metrics["val_accuracy"]:.4f}, '
                    f'LR: {train_metrics["learning_rate"]:.2e}'
                )
            
            # Save checkpoint
            if self.rank == 0:
                self._save_checkpoint(epoch, val_metrics['val_loss'], val_metrics['val_accuracy'])
            
            # Early stopping
            if self._should_early_stop(val_metrics['val_loss']):
                self.logger.info(f"Early stopping at epoch {epoch}")
                break
            
            self.current_epoch = epoch + 1
        
        if self.rank == 0:
            self.logger.info("Training completed successfully!")
    
    def _save_checkpoint(self, epoch: int, val_loss: float, val_accuracy: float):
        """Save model checkpoint"""
        is_best = val_accuracy > self.best_accuracy
        
        if is_best:
            self.best_loss = val_loss
            self.best_accuracy = val_accuracy
        
        # Get model state dict
        if isinstance(self.model, DDP):
            model_state_dict = self.model.module.state_dict()
        else:
            model_state_dict = self.model.state_dict()
        
        checkpoint = {
            'epoch': epoch,
            'model_state_dict': model_state_dict,
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict() if self.scheduler else None,
            'best_loss': self.best_loss,
            'best_accuracy': self.best_accuracy,
            'config': self.config,
            'train_metrics': self.train_metrics
        }
        
        # Save current checkpoint
        checkpoint_path = os.path.join(
            self.config['checkpoint_dir'], 
            f'checkpoint_epoch_{epoch}.pt'
        )
        torch.save(checkpoint, checkpoint_path)
        
        # Save best model
        if is_best:
            best_path = os.path.join(self.config['checkpoint_dir'], 'best_model.pt')
            torch.save(checkpoint, best_path)
            self.logger.info(f"New best model saved with accuracy: {val_accuracy:.4f}")
        
        # Save training metrics
        metrics_path = os.path.join(self.config['checkpoint_dir'], 'training_metrics.json')
        with open(metrics_path, 'w') as f:
            json.dump(self.train_metrics, f, indent=2)
    
    def _should_early_stop(self, val_loss: float, patience: int = 15, min_delta: float = 1e-4) -> bool:
        """Check if training should be stopped early"""
        if not hasattr(self, 'best_val_loss'):
            self.best_val_loss = val_loss
            self.patience_counter = 0
            return False
        
        if val_loss < self.best_val_loss - min_delta:
            self.best_val_loss = val_loss
            self.patience_counter = 0
        else:
            self.patience_counter += 1
        
        return self.patience_counter >= patience


class CompatibilityLoss(nn.Module):
    """
    Custom loss function for compatibility prediction
    Combines MSE loss with compatibility-specific constraints
    """
    
    def __init__(self, alpha: float = 1.0, beta: float = 0.5):
        super().__init__()
        
        self.alpha = alpha  # Weight for MSE loss
        self.beta = beta    # Weight for compatibility constraints
        
        self.mse_loss = nn.MSELoss()
        
    def forward(self, predictions: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        # Base MSE loss
        mse = self.mse_loss(predictions, targets)
        
        # Compatibility constraints
        # Ensure predictions are in valid range [0, 1]
        range_penalty = torch.mean(
            torch.clamp(predictions - 1, min=0) + 
            torch.clamp(-predictions, min=0)
        )
        
        # Encourage realistic compatibility distributions
        # Penalize extreme predictions (all 0s or all 1s)
        mean_pred = torch.mean(predictions, dim=-1)
        distribution_penalty = torch.mean(
            torch.abs(mean_pred - 0.5)  # Encourage predictions around 0.5
        )
        
        total_loss = (
            self.alpha * mse + 
            self.beta * range_penalty + 
            0.1 * distribution_penalty
        )
        
        return total_loss


def run_distributed_training(rank: int, world_size: int, config: Dict[str, Any]):
    """
    Function to run distributed training on a specific rank
    
    Args:
        rank: Current process rank
        world_size: Total number of processes
        config: Training configuration
    """
    # Create trainer
    trainer = DistributedCompatibilityTrainer(config, rank, world_size)
    
    # Create datasets (placeholder - implement actual dataset loading)
    train_dataset = CompatibilityDataset(config['train_data_path'])
    val_dataset = CompatibilityDataset(config['val_data_path'])
    
    # Start training
    trainer.train(train_dataset, val_dataset)
    
    # Cleanup
    if world_size > 1:
        dist.destroy_process_group()


def launch_distributed_training(config: Dict[str, Any]):
    """
    Launch distributed training across multiple GPUs
    
    Args:
        config: Training configuration dictionary
    """
    world_size = torch.cuda.device_count()
    
    if world_size <= 1:
        # Single GPU or CPU training
        run_distributed_training(0, 1, config)
    else:
        # Multi-GPU distributed training
        mp.spawn(
            run_distributed_training,
            args=(world_size, config),
            nprocs=world_size,
            join=True
        )


if __name__ == "__main__":
    # Example training configuration
    config = {
        'model': {
            'type': 'compatibility_network',
            'embedding_dim': 512,
            'num_dimensions': 12
        },
        'optimizer': {
            'type': 'adamw',
            'base_lr': 1e-4,
            'transformer_lr': 5e-5,
            'cnn_lr': 2e-4,
            'weight_decay': 1e-5
        },
        'scheduler': {
            'type': 'cosine_annealing',
            'T_0': 10,
            'T_mult': 2
        },
        'loss': {
            'type': 'compatibility_loss',
            'alpha': 1.0,
            'beta': 0.5
        },
        'batch_size': 32,
        'num_epochs': 100,
        'num_workers': 4,
        'use_amp': True,
        'log_interval': 100,
        'checkpoint_dir': './checkpoints',
        'train_data_path': './data/train',
        'val_data_path': './data/val'
    }
    
    # Create checkpoint directory
    os.makedirs(config['checkpoint_dir'], exist_ok=True)
    
    # Launch training
    launch_distributed_training(config)