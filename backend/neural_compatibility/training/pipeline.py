import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
import logging
import time
import json
import os
from datetime import datetime
import wandb
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import matplotlib.pyplot as plt
import seaborn as sns

from ..models.compatibility_network import CompatibilityNeuralNetwork, ModelFactory
from ..models.transformer import CompatibilityTransformer
from ..data.compatibility_dataset import CompatibilityDataset
from .distributed_trainer import DistributedCompatibilityTrainer

class CompatibilityTrainingPipeline:
    """
    Complete training pipeline for neural compatibility models
    Includes data loading, model training, validation, and evaluation
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Setup logging
        self._setup_logging()
        
        # Initialize tracking
        self._setup_experiment_tracking()
        
        # Training state
        self.current_epoch = 0
        self.global_step = 0
        self.best_metrics = {'loss': float('inf'), 'accuracy': 0.0}
        self.training_history = []
        
        # Performance tracking
        self.inference_times = []
        self.memory_usage = []
        
    def _setup_logging(self):
        """Setup logging configuration"""
        log_dir = self.config.get('log_dir', './logs')
        os.makedirs(log_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = os.path.join(log_dir, f'training_{timestamp}.log')
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        
    def _setup_experiment_tracking(self):
        """Setup experiment tracking with Weights & Biases"""
        if self.config.get('use_wandb', False):
            wandb.init(
                project=self.config.get('wandb_project', 'zodiac-compatibility'),
                config=self.config,
                name=self.config.get('experiment_name', None)
            )
            
    def create_model(self) -> nn.Module:
        """Create neural compatibility model based on configuration"""
        model_config = self.config['model']
        model_type = model_config.get('type', 'standard')
        
        if model_type == 'lightweight':
            model = ModelFactory.create_lightweight_model()
        elif model_type == 'standard':
            model = ModelFactory.create_standard_model()
        elif model_type == 'high_accuracy':
            model = ModelFactory.create_high_accuracy_model()
        elif model_type == 'transformer':
            model = CompatibilityTransformer(
                embed_dim=model_config.get('embed_dim', 512),
                num_layers=model_config.get('num_layers', 6),
                num_heads=model_config.get('num_heads', 8)
            )
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        model = model.to(self.device)
        
        # Log model info
        model_info = model.get_model_info() if hasattr(model, 'get_model_info') else {}
        self.logger.info(f"Created model: {model_type}")
        self.logger.info(f"Model info: {model_info}")
        
        return model
    
    def create_datasets(self) -> Tuple[Dataset, Dataset, Dataset]:
        """Create training, validation, and test datasets"""
        data_config = self.config['data']
        
        # Create datasets
        train_dataset = CompatibilityDataset(
            data_path=data_config['train_path'],
            augment=data_config.get('augment', True),
            augmentation_factor=data_config.get('augmentation_factor', 3)
        )
        
        val_dataset = CompatibilityDataset(
            data_path=data_config['val_path'],
            augment=False
        )
        
        test_dataset = CompatibilityDataset(
            data_path=data_config['test_path'],
            augment=False
        )
        
        self.logger.info(f"Dataset sizes - Train: {len(train_dataset)}, "
                        f"Val: {len(val_dataset)}, Test: {len(test_dataset)}")
        
        return train_dataset, val_dataset, test_dataset
    
    def create_data_loaders(self, train_dataset: Dataset, val_dataset: Dataset, 
                          test_dataset: Dataset) -> Tuple[DataLoader, DataLoader, DataLoader]:
        """Create data loaders for training, validation, and testing"""
        batch_size = self.config.get('batch_size', 32)
        num_workers = self.config.get('num_workers', 4)
        
        train_loader = DataLoader(
            train_dataset,
            batch_size=batch_size,
            shuffle=True,
            num_workers=num_workers,
            pin_memory=True,
            drop_last=True
        )
        
        val_loader = DataLoader(
            val_dataset,
            batch_size=batch_size,
            shuffle=False,
            num_workers=num_workers,
            pin_memory=True
        )
        
        test_loader = DataLoader(
            test_dataset,
            batch_size=batch_size,
            shuffle=False,
            num_workers=num_workers,
            pin_memory=True
        )
        
        return train_loader, val_loader, test_loader
    
    def train_epoch(self, model: nn.Module, train_loader: DataLoader, 
                   optimizer: torch.optim.Optimizer, criterion: nn.Module,
                   epoch: int) -> Dict[str, float]:
        """Train model for one epoch"""
        model.train()
        
        total_loss = 0.0
        total_accuracy = 0.0
        total_samples = 0
        batch_times = []
        
        start_time = time.time()
        
        for batch_idx, batch in enumerate(train_loader):
            batch_start = time.time()
            
            # Move batch to device
            sign1_idx = batch['sign1_idx'].to(self.device)
            sign2_idx = batch['sign2_idx'].to(self.device)
            aspect_matrix = batch['aspect_matrix'].to(self.device)
            context_features = batch['context_features'].to(self.device)
            targets = batch['targets'].to(self.device)
            
            # Forward pass
            optimizer.zero_grad()
            
            if hasattr(model, 'forward'):
                outputs = model(sign1_idx, sign2_idx, aspect_matrix, context_features)
            else:
                outputs = model(sign1_idx, sign2_idx, aspect_matrix, context_features)
            
            # Calculate loss
            if isinstance(outputs, dict):
                # Handle transformer outputs
                loss = 0
                for dimension, predictions in outputs.items():
                    if dimension != 'attention_weights':
                        dim_idx = self._get_dimension_index(dimension)
                        if dim_idx is not None:
                            loss += criterion(predictions, targets[:, dim_idx])
                loss /= (len(outputs) - 1)  # Average across dimensions (exclude attention_weights)
            else:
                loss = criterion(outputs, targets)
            
            # Backward pass
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            
            # Calculate metrics
            batch_size = targets.size(0)
            total_loss += loss.item() * batch_size
            total_samples += batch_size
            
            # Calculate accuracy
            with torch.no_grad():
                if isinstance(outputs, dict):
                    # Average accuracy across dimensions
                    accuracies = []
                    for dimension, predictions in outputs.items():
                        if dimension != 'attention_weights':
                            dim_idx = self._get_dimension_index(dimension)
                            if dim_idx is not None:
                                acc = self._calculate_accuracy(predictions, targets[:, dim_idx])
                                accuracies.append(acc)
                    accuracy = np.mean(accuracies) if accuracies else 0.0
                else:
                    accuracy = self._calculate_accuracy(outputs, targets)
                
                total_accuracy += accuracy * batch_size
            
            batch_times.append(time.time() - batch_start)
            
            # Log progress
            if batch_idx % self.config.get('log_interval', 100) == 0:
                elapsed = time.time() - start_time
                samples_per_sec = total_samples / elapsed if elapsed > 0 else 0
                
                self.logger.info(
                    f'Epoch: {epoch:>3d}, Batch: {batch_idx:>6d}/{len(train_loader)}, '
                    f'Loss: {loss.item():.6f}, Accuracy: {accuracy:.4f}, '
                    f'Samples/sec: {samples_per_sec:.1f}'
                )
            
            self.global_step += 1
        
        # Calculate epoch metrics
        avg_loss = total_loss / total_samples
        avg_accuracy = total_accuracy / total_samples
        avg_batch_time = np.mean(batch_times)
        
        return {
            'train_loss': avg_loss,
            'train_accuracy': avg_accuracy,
            'avg_batch_time': avg_batch_time,
            'samples_per_sec': total_samples / (time.time() - start_time)
        }
    
    def validate_epoch(self, model: nn.Module, val_loader: DataLoader, 
                      criterion: nn.Module, epoch: int) -> Dict[str, float]:
        """Validate model for one epoch"""
        model.eval()
        
        total_loss = 0.0
        total_accuracy = 0.0
        total_samples = 0
        inference_times = []
        
        all_predictions = []
        all_targets = []
        
        with torch.no_grad():
            for batch in val_loader:
                # Move batch to device
                sign1_idx = batch['sign1_idx'].to(self.device)
                sign2_idx = batch['sign2_idx'].to(self.device)
                aspect_matrix = batch['aspect_matrix'].to(self.device)
                context_features = batch['context_features'].to(self.device)
                targets = batch['targets'].to(self.device)
                
                # Measure inference time
                inference_start = time.time()
                
                # Forward pass
                outputs = model(sign1_idx, sign2_idx, aspect_matrix, context_features)
                
                inference_time = time.time() - inference_start
                inference_times.append(inference_time)
                
                # Calculate loss
                if isinstance(outputs, dict):
                    loss = 0
                    predictions = []
                    for dimension, preds in outputs.items():
                        if dimension != 'attention_weights':
                            dim_idx = self._get_dimension_index(dimension)
                            if dim_idx is not None:
                                loss += criterion(preds, targets[:, dim_idx])
                                predictions.append(preds.unsqueeze(1))
                    
                    if predictions:
                        loss /= len(predictions)
                        predictions = torch.cat(predictions, dim=1)
                    else:
                        predictions = torch.zeros_like(targets)
                else:
                    loss = criterion(outputs, targets)
                    predictions = outputs
                
                # Store predictions and targets for detailed analysis
                all_predictions.append(predictions.cpu())
                all_targets.append(targets.cpu())
                
                # Update metrics
                batch_size = targets.size(0)
                total_loss += loss.item() * batch_size
                total_samples += batch_size
                
                # Calculate accuracy
                accuracy = self._calculate_accuracy(predictions, targets)
                total_accuracy += accuracy * batch_size
        
        # Calculate metrics
        avg_loss = total_loss / total_samples
        avg_accuracy = total_accuracy / total_samples
        avg_inference_time = np.mean(inference_times) * 1000  # Convert to ms
        
        # Store inference times for performance analysis
        self.inference_times.extend(inference_times)
        
        # Detailed analysis
        all_predictions = torch.cat(all_predictions, dim=0)
        all_targets = torch.cat(all_targets, dim=0)
        
        detailed_metrics = self._calculate_detailed_metrics(all_predictions, all_targets)
        
        validation_metrics = {
            'val_loss': avg_loss,
            'val_accuracy': avg_accuracy,
            'avg_inference_time_ms': avg_inference_time,
            **detailed_metrics
        }
        
        return validation_metrics
    
    def _get_dimension_index(self, dimension: str) -> Optional[int]:
        """Map dimension name to index"""
        dimension_map = {
            'love': 0, 'friendship': 1, 'communication': 2, 'emotional': 3,
            'intellectual': 4, 'physical': 5, 'spiritual': 6, 'career': 7,
            'family': 8, 'trust': 9, 'values': 10, 'overall': 11
        }
        return dimension_map.get(dimension)
    
    def _calculate_accuracy(self, predictions: torch.Tensor, targets: torch.Tensor, 
                          tolerance: float = 0.1) -> float:
        """Calculate accuracy with tolerance for regression"""
        correct = torch.abs(predictions - targets) <= tolerance
        accuracy = correct.float().mean().item()
        return accuracy
    
    def _calculate_detailed_metrics(self, predictions: torch.Tensor, 
                                  targets: torch.Tensor) -> Dict[str, float]:
        """Calculate detailed metrics for evaluation"""
        # Convert to numpy
        pred_np = predictions.numpy()
        target_np = targets.numpy()
        
        metrics = {}
        
        # Per-dimension metrics
        dimension_names = ['love', 'friendship', 'communication', 'emotional',
                          'intellectual', 'physical', 'spiritual', 'career',
                          'family', 'trust', 'values', 'overall']
        
        for i, dim_name in enumerate(dimension_names):
            if i < pred_np.shape[1]:
                # Mean Absolute Error
                mae = np.mean(np.abs(pred_np[:, i] - target_np[:, i]))
                metrics[f'{dim_name}_mae'] = mae
                
                # Mean Squared Error
                mse = np.mean((pred_np[:, i] - target_np[:, i]) ** 2)
                metrics[f'{dim_name}_mse'] = mse
                
                # Correlation
                corr = np.corrcoef(pred_np[:, i], target_np[:, i])[0, 1]
                metrics[f'{dim_name}_correlation'] = corr if not np.isnan(corr) else 0.0
        
        # Overall metrics
        overall_mae = np.mean(np.abs(pred_np - target_np))
        overall_mse = np.mean((pred_np - target_np) ** 2)
        
        metrics.update({
            'overall_mae': overall_mae,
            'overall_mse': overall_mse,
            'overall_rmse': np.sqrt(overall_mse)
        })
        
        return metrics
    
    def run_training(self) -> Dict[str, Any]:
        """Run complete training pipeline"""
        self.logger.info("Starting neural compatibility training pipeline")
        
        # Create model
        model = self.create_model()
        
        # Create datasets and data loaders
        train_dataset, val_dataset, test_dataset = self.create_datasets()
        train_loader, val_loader, test_loader = self.create_data_loaders(
            train_dataset, val_dataset, test_dataset
        )
        
        # Create optimizer and scheduler
        optimizer = self._create_optimizer(model)
        scheduler = self._create_scheduler(optimizer)
        criterion = self._create_criterion()
        
        # Training loop
        num_epochs = self.config.get('num_epochs', 100)
        
        for epoch in range(num_epochs):
            # Train epoch
            train_metrics = self.train_epoch(model, train_loader, optimizer, criterion, epoch)
            
            # Validate epoch
            val_metrics = self.validate_epoch(model, val_loader, criterion, epoch)
            
            # Update scheduler
            if scheduler is not None:
                if isinstance(scheduler, torch.optim.lr_scheduler.ReduceLROnPlateau):
                    scheduler.step(val_metrics['val_loss'])
                else:
                    scheduler.step()
            
            # Combine metrics
            epoch_metrics = {
                **train_metrics,
                **val_metrics,
                'epoch': epoch,
                'learning_rate': optimizer.param_groups[0]['lr']
            }
            
            # Log metrics
            self._log_epoch_metrics(epoch_metrics)
            
            # Save checkpoint
            self._save_checkpoint(model, optimizer, epoch, epoch_metrics)
            
            # Check for early stopping
            if self._should_early_stop(val_metrics['val_loss']):
                self.logger.info(f"Early stopping at epoch {epoch}")
                break
        
        # Final evaluation
        test_metrics = self.evaluate_model(model, test_loader, criterion)
        
        # Performance analysis
        performance_report = self._generate_performance_report(model)
        
        final_results = {
            'training_completed': True,
            'final_train_metrics': train_metrics,
            'final_val_metrics': val_metrics,
            'test_metrics': test_metrics,
            'performance_report': performance_report,
            'training_history': self.training_history
        }
        
        self.logger.info("Training pipeline completed successfully!")
        
        return final_results
    
    def evaluate_model(self, model: nn.Module, test_loader: DataLoader, 
                      criterion: nn.Module) -> Dict[str, float]:
        """Comprehensive model evaluation"""
        self.logger.info("Running comprehensive model evaluation")
        
        model.eval()
        total_loss = 0.0
        total_accuracy = 0.0
        total_samples = 0
        
        all_predictions = []
        all_targets = []
        inference_times = []
        
        with torch.no_grad():
            for batch in test_loader:
                # Prepare batch
                sign1_idx = batch['sign1_idx'].to(self.device)
                sign2_idx = batch['sign2_idx'].to(self.device)
                aspect_matrix = batch['aspect_matrix'].to(self.device)
                context_features = batch['context_features'].to(self.device)
                targets = batch['targets'].to(self.device)
                
                # Measure inference time
                start_time = time.time()
                outputs = model(sign1_idx, sign2_idx, aspect_matrix, context_features)
                inference_time = time.time() - start_time
                inference_times.append(inference_time)
                
                # Process outputs
                if isinstance(outputs, dict):
                    predictions = []
                    for dimension, preds in outputs.items():
                        if dimension != 'attention_weights':
                            predictions.append(preds.unsqueeze(1))
                    predictions = torch.cat(predictions, dim=1) if predictions else torch.zeros_like(targets)
                else:
                    predictions = outputs
                
                # Store for analysis
                all_predictions.append(predictions.cpu())
                all_targets.append(targets.cpu())
                
                # Calculate loss and accuracy
                loss = criterion(predictions, targets)
                accuracy = self._calculate_accuracy(predictions, targets)
                
                batch_size = targets.size(0)
                total_loss += loss.item() * batch_size
                total_accuracy += accuracy * batch_size
                total_samples += batch_size
        
        # Calculate final metrics
        test_loss = total_loss / total_samples
        test_accuracy = total_accuracy / total_samples
        avg_inference_time = np.mean(inference_times) * 1000  # ms
        
        # Detailed analysis
        all_predictions = torch.cat(all_predictions, dim=0)
        all_targets = torch.cat(all_targets, dim=0)
        detailed_metrics = self._calculate_detailed_metrics(all_predictions, all_targets)
        
        test_metrics = {
            'test_loss': test_loss,
            'test_accuracy': test_accuracy,
            'avg_inference_time_ms': avg_inference_time,
            'inference_under_400ms': (avg_inference_time < 400),
            **detailed_metrics
        }
        
        return test_metrics
    
    def _create_optimizer(self, model: nn.Module) -> torch.optim.Optimizer:
        """Create optimizer"""
        opt_config = self.config.get('optimizer', {})
        opt_type = opt_config.get('type', 'adamw')
        
        if opt_type == 'adamw':
            return torch.optim.AdamW(
                model.parameters(),
                lr=opt_config.get('learning_rate', 1e-4),
                weight_decay=opt_config.get('weight_decay', 1e-5)
            )
        elif opt_type == 'adam':
            return torch.optim.Adam(
                model.parameters(),
                lr=opt_config.get('learning_rate', 1e-4)
            )
        else:
            raise ValueError(f"Unknown optimizer type: {opt_type}")
    
    def _create_scheduler(self, optimizer: torch.optim.Optimizer) -> Optional[torch.optim.lr_scheduler._LRScheduler]:
        """Create learning rate scheduler"""
        sched_config = self.config.get('scheduler', {})
        sched_type = sched_config.get('type')
        
        if not sched_type:
            return None
        
        if sched_type == 'cosine':
            return torch.optim.lr_scheduler.CosineAnnealingLR(
                optimizer,
                T_max=self.config.get('num_epochs', 100),
                eta_min=sched_config.get('eta_min', 1e-6)
            )
        elif sched_type == 'reduce_on_plateau':
            return torch.optim.lr_scheduler.ReduceLROnPlateau(
                optimizer,
                mode='min',
                factor=sched_config.get('factor', 0.5),
                patience=sched_config.get('patience', 10)
            )
        else:
            return None
    
    def _create_criterion(self) -> nn.Module:
        """Create loss criterion"""
        return nn.MSELoss()
    
    def _log_epoch_metrics(self, metrics: Dict[str, float]):
        """Log epoch metrics"""
        # Console logging
        self.logger.info(
            f"Epoch {metrics['epoch']:>3d}: "
            f"Train Loss: {metrics['train_loss']:.6f}, "
            f"Val Loss: {metrics['val_loss']:.6f}, "
            f"Train Acc: {metrics['train_accuracy']:.4f}, "
            f"Val Acc: {metrics['val_accuracy']:.4f}, "
            f"Inference: {metrics.get('avg_inference_time_ms', 0):.1f}ms"
        )
        
        # Wandb logging
        if self.config.get('use_wandb', False):
            wandb.log(metrics)
        
        # Store in history
        self.training_history.append(metrics)
    
    def _save_checkpoint(self, model: nn.Module, optimizer: torch.optim.Optimizer, 
                        epoch: int, metrics: Dict[str, float]):
        """Save model checkpoint"""
        if metrics['val_accuracy'] > self.best_metrics['accuracy']:
            self.best_metrics = {
                'loss': metrics['val_loss'],
                'accuracy': metrics['val_accuracy']
            }
            
            checkpoint_dir = self.config.get('checkpoint_dir', './checkpoints')
            os.makedirs(checkpoint_dir, exist_ok=True)
            
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'metrics': metrics,
                'config': self.config
            }, os.path.join(checkpoint_dir, 'best_model.pt'))
    
    def _should_early_stop(self, val_loss: float, patience: int = 15) -> bool:
        """Check for early stopping"""
        if not hasattr(self, '_early_stop_counter'):
            self._early_stop_counter = 0
            self._best_val_loss = val_loss
            
        if val_loss < self._best_val_loss:
            self._best_val_loss = val_loss
            self._early_stop_counter = 0
        else:
            self._early_stop_counter += 1
            
        return self._early_stop_counter >= patience
    
    def _generate_performance_report(self, model: nn.Module) -> Dict[str, Any]:
        """Generate performance analysis report"""
        # Model size analysis
        param_count = sum(p.numel() for p in model.parameters())
        model_size_mb = param_count * 4 / 1024 / 1024  # Assuming float32
        
        # Inference speed analysis
        avg_inference_time = np.mean(self.inference_times) * 1000 if self.inference_times else 0
        p95_inference_time = np.percentile(self.inference_times, 95) * 1000 if self.inference_times else 0
        
        report = {
            'model_parameters': param_count,
            'model_size_mb': model_size_mb,
            'avg_inference_time_ms': avg_inference_time,
            'p95_inference_time_ms': p95_inference_time,
            'meets_performance_target': avg_inference_time < 400,  # <400ms target
            'memory_efficient': model_size_mb < 200,  # <200MB target
            'accuracy_target_met': self.best_metrics['accuracy'] > 0.96  # >96% target
        }
        
        return report


if __name__ == "__main__":
    # Example training configuration
    config = {
        'model': {
            'type': 'standard',
        },
        'data': {
            'train_path': './data/train',
            'val_path': './data/val',
            'test_path': './data/test',
            'augment': True,
            'augmentation_factor': 3
        },
        'optimizer': {
            'type': 'adamw',
            'learning_rate': 1e-4,
            'weight_decay': 1e-5
        },
        'scheduler': {
            'type': 'cosine',
            'eta_min': 1e-6
        },
        'batch_size': 32,
        'num_epochs': 100,
        'num_workers': 4,
        'log_interval': 100,
        'use_wandb': False,
        'checkpoint_dir': './checkpoints'
    }
    
    # Create and run training pipeline
    pipeline = CompatibilityTrainingPipeline(config)
    results = pipeline.run_training()
    
    print("Training completed!")
    print(f"Best validation accuracy: {results['final_val_metrics']['val_accuracy']:.4f}")
    print(f"Test accuracy: {results['test_metrics']['test_accuracy']:.4f}")
    print(f"Inference time: {results['test_metrics']['avg_inference_time_ms']:.1f}ms")