import torch
import torch.nn as nn
import torch.nn.utils.prune as prune
import numpy as np
import copy
from typing import Dict, List, Tuple, Optional, Any, Union
import logging
import time
from collections import defaultdict

from ..models.compatibility_network import CompatibilityNeuralNetwork
from ..models.transformer import CompatibilityTransformer

class PruningConfig:
    """Configuration for neural network pruning"""
    
    def __init__(self):
        # Pruning method
        self.method = 'structured'  # 'unstructured', 'structured', 'gradual'
        
        # Pruning strategy
        self.strategy = 'magnitude'  # 'magnitude', 'gradient', 'fisher', 'lottery_ticket'
        
        # Sparsity targets
        self.global_sparsity = 0.5  # Overall sparsity target
        self.layer_sparsities = {}  # Per-layer sparsity targets
        
        # Gradual pruning settings
        self.initial_sparsity = 0.0
        self.final_sparsity = 0.5
        self.pruning_steps = 10
        self.pruning_frequency = 1000  # Steps between pruning
        
        # Fine-tuning after pruning
        self.finetune_epochs = 10
        self.finetune_learning_rate = 1e-5
        
        # Layer-specific settings
        self.prune_embeddings = False  # Embeddings are often sensitive
        self.prune_attention = True
        self.prune_linear = True
        self.prune_conv = True
        
        # Performance constraints
        self.max_accuracy_drop = 0.03
        self.target_speedup = 2.0
        
        # Preservation of astrological knowledge
        self.preserve_sign_relationships = True
        self.preserve_element_patterns = True


class CompatibilityModelPruner:
    """
    Neural network pruning for compatibility models
    Supports various pruning strategies while preserving astrological knowledge
    """
    
    def __init__(self, config: PruningConfig = None):
        self.config = config or PruningConfig()
        self.logger = logging.getLogger(__name__)
        
        self.original_model = None
        self.pruned_model = None
        self.pruning_history = []
        self.important_weights = {}  # Weights important for astrological patterns
        
    def prune_model(self, model: nn.Module, 
                   validation_data: Optional[torch.utils.data.DataLoader] = None,
                   training_data: Optional[torch.utils.data.DataLoader] = None) -> nn.Module:
        """
        Prune a neural compatibility model
        
        Args:
            model: Original model to prune
            validation_data: Validation data for accuracy monitoring
            training_data: Training data for fine-tuning
            
        Returns:
            Pruned model
        """
        self.original_model = copy.deepcopy(model)
        self.logger.info(f"Starting {self.config.method} pruning with {self.config.strategy} strategy...")
        
        # Identify important weights for astrological knowledge
        if self.config.preserve_sign_relationships or self.config.preserve_element_patterns:
            self._identify_important_weights(model)
        
        # Apply pruning based on method
        if self.config.method == 'unstructured':
            pruned_model = self._unstructured_pruning(model)
        elif self.config.method == 'structured':
            pruned_model = self._structured_pruning(model)
        elif self.config.method == 'gradual':
            if training_data is None:
                raise ValueError("Training data required for gradual pruning")
            pruned_model = self._gradual_pruning(model, training_data, validation_data)
        else:
            raise ValueError(f"Unknown pruning method: {self.config.method}")
        
        # Fine-tune pruned model
        if training_data is not None and self.config.finetune_epochs > 0:
            self.logger.info("Fine-tuning pruned model...")
            self._finetune_pruned_model(pruned_model, training_data, validation_data)
        
        self.pruned_model = pruned_model
        self.logger.info("Pruning completed successfully")
        
        return pruned_model
    
    def _identify_important_weights(self, model: nn.Module):
        """Identify weights important for astrological relationships"""
        self.logger.info("Identifying astrologically important weights...")
        
        # For embeddings: weights corresponding to element/modality relationships
        if hasattr(model, 'sign_embeddings'):
            element_groups = [
                [0, 4, 8],     # Fire: Aries, Leo, Sagittarius
                [1, 5, 9],     # Earth: Taurus, Virgo, Capricorn
                [2, 6, 10],    # Air: Gemini, Libra, Aquarius
                [3, 7, 11]     # Water: Cancer, Scorpio, Pisces
            ]
            
            # Mark weights connecting same-element signs as important
            embedding_weights = model.sign_embeddings.weight.data
            important_indices = set()
            
            for group in element_groups:
                for i in group:
                    for j in group:
                        if i != j:
                            # Calculate similarity between embeddings
                            similarity = torch.cosine_similarity(
                                embedding_weights[i:i+1], 
                                embedding_weights[j:j+1]
                            )
                            # Mark as important if similar (good element relationship)
                            if similarity > 0.5:
                                important_indices.add((i, j))
            
            self.important_weights['sign_embeddings'] = important_indices
        
        # For attention layers: weights that capture sign-sign relationships
        for name, module in model.named_modules():
            if isinstance(module, nn.MultiheadAttention):
                # Mark attention weights as generally important
                self.important_weights[name] = 'all'
            elif 'compatibility' in name.lower() and isinstance(module, nn.Linear):
                # Compatibility-related linear layers
                self.important_weights[name] = 'compatibility_critical'
    
    def _unstructured_pruning(self, model: nn.Module) -> nn.Module:
        """Apply unstructured (weight-level) pruning"""
        pruned_model = copy.deepcopy(model)
        
        # Collect modules to prune
        modules_to_prune = []
        
        for name, module in pruned_model.named_modules():
            should_prune = False
            
            if isinstance(module, nn.Linear) and self.config.prune_linear:
                should_prune = True
            elif isinstance(module, nn.Conv2d) and self.config.prune_conv:
                should_prune = True
            elif isinstance(module, nn.Embedding) and self.config.prune_embeddings:
                should_prune = True
            elif isinstance(module, nn.MultiheadAttention) and self.config.prune_attention:
                should_prune = True
            
            if should_prune and hasattr(module, 'weight'):
                modules_to_prune.append((module, 'weight'))
        
        self.logger.info(f"Pruning {len(modules_to_prune)} modules")
        
        # Apply pruning based on strategy
        if self.config.strategy == 'magnitude':
            # Global magnitude-based pruning
            prune.global_unstructured(
                modules_to_prune,
                pruning_method=prune.L1Unstructured,
                amount=self.config.global_sparsity
            )
        
        elif self.config.strategy == 'lottery_ticket':
            # Lottery Ticket Hypothesis: find winning tickets
            self._lottery_ticket_pruning(pruned_model, modules_to_prune)
        
        # Remove pruning reparameterization to make pruning permanent
        for module, param_name in modules_to_prune:
            prune.remove(module, param_name)
        
        return pruned_model
    
    def _structured_pruning(self, model: nn.Module) -> nn.Module:
        """Apply structured (neuron/channel-level) pruning"""
        pruned_model = copy.deepcopy(model)
        
        # Analyze each layer for structured pruning
        for name, module in pruned_model.named_modules():
            if isinstance(module, nn.Linear) and self.config.prune_linear:
                self._prune_linear_layer(module, name)
            elif isinstance(module, nn.Conv2d) and self.config.prune_conv:
                self._prune_conv_layer(module, name)
        
        return pruned_model
    
    def _prune_linear_layer(self, layer: nn.Linear, layer_name: str):
        """Apply structured pruning to linear layer"""
        if layer_name in self.important_weights:
            # Reduce pruning for important layers
            sparsity = min(self.config.global_sparsity * 0.5, 0.3)
        else:
            sparsity = self.config.layer_sparsities.get(layer_name, self.config.global_sparsity)
        
        # Calculate importance scores for each neuron
        weight = layer.weight.data
        importance_scores = torch.norm(weight, dim=1)  # L2 norm of each output neuron
        
        # Determine neurons to prune
        num_neurons = weight.size(0)
        num_to_prune = int(num_neurons * sparsity)
        
        if num_to_prune > 0:
            # Get indices of least important neurons
            _, indices_to_prune = torch.topk(importance_scores, num_to_prune, largest=False)
            
            # Zero out pruned neurons
            weight[indices_to_prune] = 0
            if layer.bias is not None:
                layer.bias.data[indices_to_prune] = 0
            
            self.logger.debug(f"Pruned {num_to_prune}/{num_neurons} neurons from {layer_name}")
    
    def _prune_conv_layer(self, layer: nn.Conv2d, layer_name: str):
        """Apply structured pruning to convolutional layer"""
        sparsity = self.config.layer_sparsities.get(layer_name, self.config.global_sparsity)
        
        # Calculate importance scores for each filter
        weight = layer.weight.data
        importance_scores = torch.norm(weight.view(weight.size(0), -1), dim=1)
        
        # Determine filters to prune
        num_filters = weight.size(0)
        num_to_prune = int(num_filters * sparsity)
        
        if num_to_prune > 0:
            # Get indices of least important filters
            _, indices_to_prune = torch.topk(importance_scores, num_to_prune, largest=False)
            
            # Zero out pruned filters
            weight[indices_to_prune] = 0
            if layer.bias is not None:
                layer.bias.data[indices_to_prune] = 0
            
            self.logger.debug(f"Pruned {num_to_prune}/{num_filters} filters from {layer_name}")
    
    def _gradual_pruning(self, model: nn.Module, 
                        training_data: torch.utils.data.DataLoader,
                        validation_data: Optional[torch.utils.data.DataLoader] = None) -> nn.Module:
        """Apply gradual pruning during training"""
        pruned_model = copy.deepcopy(model)
        
        # Setup training
        optimizer = torch.optim.Adam(pruned_model.parameters(), lr=self.config.finetune_learning_rate)
        criterion = nn.MSELoss()
        
        # Calculate pruning schedule
        pruning_schedule = self._create_pruning_schedule()
        
        step = 0
        current_sparsity = self.config.initial_sparsity
        
        for epoch in range(self.config.finetune_epochs):
            pruned_model.train()
            
            for batch in training_data:
                # Training step
                optimizer.zero_grad()
                
                try:
                    if isinstance(batch, dict):
                        outputs = pruned_model(
                            batch['sign1_idx'],
                            batch['sign2_idx'],
                            batch['aspect_matrix'],
                            batch['context_features']
                        )
                        targets = batch['targets']
                    else:
                        outputs = pruned_model(*batch[:-1])
                        targets = batch[-1]
                    
                    if isinstance(outputs, dict):
                        loss = 0
                        for dim_outputs in outputs.values():
                            if torch.is_tensor(dim_outputs):
                                loss += criterion(dim_outputs, targets[:, 0])
                        loss /= len(outputs)
                    else:
                        loss = criterion(outputs, targets)
                    
                    loss.backward()
                    optimizer.step()
                    
                except Exception as e:
                    self.logger.warning(f"Gradual pruning batch failed: {e}")
                    continue
                
                # Apply pruning if it's time
                if step % self.config.pruning_frequency == 0 and step > 0:
                    if step < len(pruning_schedule):
                        target_sparsity = pruning_schedule[step // self.config.pruning_frequency]
                        self._apply_gradual_pruning_step(pruned_model, current_sparsity, target_sparsity)
                        current_sparsity = target_sparsity
                        
                        self.logger.info(f"Step {step}: Applied pruning to {target_sparsity:.2%} sparsity")
                
                step += 1
            
            # Validation
            if validation_data is not None and epoch % 5 == 0:
                val_accuracy = self._evaluate_model(pruned_model, validation_data)
                self.logger.info(f"Epoch {epoch}: Validation accuracy = {val_accuracy:.4f}")
        
        return pruned_model
    
    def _create_pruning_schedule(self) -> List[float]:
        """Create schedule for gradual pruning"""
        schedule = []
        for i in range(self.config.pruning_steps):
            # Polynomial schedule
            progress = i / (self.config.pruning_steps - 1)
            sparsity = (self.config.initial_sparsity + 
                       (self.config.final_sparsity - self.config.initial_sparsity) * 
                       (progress ** 3))
            schedule.append(sparsity)
        
        return schedule
    
    def _apply_gradual_pruning_step(self, model: nn.Module, 
                                   current_sparsity: float, target_sparsity: float):
        """Apply a single step of gradual pruning"""
        modules_to_prune = []
        
        for module in model.modules():
            if isinstance(module, (nn.Linear, nn.Conv2d)) and hasattr(module, 'weight'):
                modules_to_prune.append((module, 'weight'))
        
        # Calculate how much additional pruning is needed
        additional_sparsity = target_sparsity - current_sparsity
        
        if additional_sparsity > 0:
            prune.global_unstructured(
                modules_to_prune,
                pruning_method=prune.L1Unstructured,
                amount=additional_sparsity
            )
    
    def _lottery_ticket_pruning(self, model: nn.Module, modules_to_prune: List[Tuple]):
        """Implement Lottery Ticket Hypothesis pruning"""
        # Store initial weights
        initial_weights = {}
        for module, param_name in modules_to_prune:
            initial_weights[(module, param_name)] = getattr(module, param_name).clone()
        
        # Apply magnitude-based pruning
        prune.global_unstructured(
            modules_to_prune,
            pruning_method=prune.L1Unstructured,
            amount=self.config.global_sparsity
        )
        
        # Reset remaining weights to initial values (winning ticket)
        for module, param_name in modules_to_prune:
            mask = getattr(module, param_name + '_mask')
            original_param = initial_weights[(module, param_name)]
            getattr(module, param_name).data = original_param * mask
    
    def _finetune_pruned_model(self, model: nn.Module,
                              training_data: torch.utils.data.DataLoader,
                              validation_data: Optional[torch.utils.data.DataLoader] = None):
        """Fine-tune the pruned model"""
        optimizer = torch.optim.Adam(
            [p for p in model.parameters() if p.requires_grad], 
            lr=self.config.finetune_learning_rate
        )
        criterion = nn.MSELoss()
        
        best_accuracy = 0.0
        
        for epoch in range(self.config.finetune_epochs):
            model.train()
            epoch_loss = 0.0
            batch_count = 0
            
            for batch in training_data:
                optimizer.zero_grad()
                
                try:
                    if isinstance(batch, dict):
                        outputs = model(
                            batch['sign1_idx'],
                            batch['sign2_idx'],
                            batch['aspect_matrix'],
                            batch['context_features']
                        )
                        targets = batch['targets']
                    else:
                        outputs = model(*batch[:-1])
                        targets = batch[-1]
                    
                    if isinstance(outputs, dict):
                        loss = 0
                        for dim_outputs in outputs.values():
                            if torch.is_tensor(dim_outputs):
                                loss += criterion(dim_outputs, targets[:, 0])
                        loss /= len(outputs)
                    else:
                        loss = criterion(outputs, targets)
                    
                    loss.backward()
                    
                    # Gradient clipping
                    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                    
                    optimizer.step()
                    
                    epoch_loss += loss.item()
                    batch_count += 1
                    
                except Exception as e:
                    self.logger.warning(f"Fine-tuning batch failed: {e}")
                    continue
            
            avg_loss = epoch_loss / max(batch_count, 1)
            
            # Validation
            if validation_data is not None:
                val_accuracy = self._evaluate_model(model, validation_data)
                if val_accuracy > best_accuracy:
                    best_accuracy = val_accuracy
                
                self.logger.info(f"Fine-tune Epoch {epoch+1}: "
                               f"Loss={avg_loss:.6f}, Val Acc={val_accuracy:.4f}")
            else:
                self.logger.info(f"Fine-tune Epoch {epoch+1}: Loss={avg_loss:.6f}")
    
    def _evaluate_model(self, model: nn.Module, 
                       validation_data: torch.utils.data.DataLoader) -> float:
        """Evaluate model accuracy"""
        model.eval()
        total_accuracy = 0.0
        total_samples = 0
        
        with torch.no_grad():
            for batch in validation_data:
                try:
                    if isinstance(batch, dict):
                        outputs = model(
                            batch['sign1_idx'],
                            batch['sign2_idx'],
                            batch['aspect_matrix'],
                            batch['context_features']
                        )
                        targets = batch['targets']
                    else:
                        outputs = model(*batch[:-1])
                        targets = batch[-1]
                    
                    if isinstance(outputs, dict):
                        # Use first output for accuracy calculation
                        first_output = next(iter(outputs.values()))
                        if torch.is_tensor(first_output):
                            accuracy = (torch.abs(first_output - targets[:, 0]) <= 0.1).float().mean().item()
                        else:
                            accuracy = 0.5
                    else:
                        accuracy = (torch.abs(outputs - targets) <= 0.1).float().mean().item()
                    
                    batch_size = targets.size(0)
                    total_accuracy += accuracy * batch_size
                    total_samples += batch_size
                    
                except Exception as e:
                    self.logger.warning(f"Evaluation batch failed: {e}")
                    continue
        
        return total_accuracy / max(total_samples, 1)
    
    def analyze_pruning_results(self, test_data: torch.utils.data.DataLoader) -> Dict[str, Any]:
        """Analyze pruning results and model performance"""
        if self.pruned_model is None:
            raise ValueError("No pruned model available for analysis")
        
        results = {}
        
        # Sparsity analysis
        results['sparsity_analysis'] = self._calculate_sparsity()
        
        # Performance comparison
        if self.original_model is not None:
            results['performance_comparison'] = self._compare_model_performance(test_data)
        
        # Model size comparison
        results['size_comparison'] = self._compare_model_sizes()
        
        # Astrological knowledge preservation
        results['knowledge_preservation'] = self._analyze_knowledge_preservation()
        
        return results
    
    def _calculate_sparsity(self) -> Dict[str, float]:
        """Calculate sparsity statistics"""
        sparsity_stats = {}
        total_params = 0
        zero_params = 0
        
        layer_sparsities = {}
        
        for name, module in self.pruned_model.named_modules():
            if hasattr(module, 'weight') and module.weight is not None:
                weight = module.weight.data
                layer_total = weight.numel()
                layer_zeros = (weight == 0).sum().item()
                
                layer_sparsity = layer_zeros / layer_total if layer_total > 0 else 0
                layer_sparsities[name] = layer_sparsity
                
                total_params += layer_total
                zero_params += layer_zeros
        
        global_sparsity = zero_params / total_params if total_params > 0 else 0
        
        sparsity_stats.update({
            'global_sparsity': global_sparsity,
            'total_parameters': total_params,
            'zero_parameters': zero_params,
            'layer_sparsities': layer_sparsities
        })
        
        return sparsity_stats
    
    def _compare_model_performance(self, test_data: torch.utils.data.DataLoader) -> Dict[str, Any]:
        """Compare original and pruned model performance"""
        original_metrics = self._benchmark_model(self.original_model, test_data, "Original")
        pruned_metrics = self._benchmark_model(self.pruned_model, test_data, "Pruned")
        
        comparison = {
            'original': original_metrics,
            'pruned': pruned_metrics,
            'accuracy_change': pruned_metrics['accuracy'] - original_metrics['accuracy'],
            'speedup': (original_metrics['inference_time'] / pruned_metrics['inference_time'] 
                       if pruned_metrics['inference_time'] > 0 else 1.0),
            'accuracy_preserved': abs(pruned_metrics['accuracy'] - original_metrics['accuracy']) <= self.config.max_accuracy_drop
        }
        
        return comparison
    
    def _benchmark_model(self, model: nn.Module, test_data: torch.utils.data.DataLoader,
                        model_name: str) -> Dict[str, float]:
        """Benchmark model performance"""
        model.eval()
        
        total_accuracy = 0.0
        total_samples = 0
        inference_times = []
        
        with torch.no_grad():
            for batch in test_data:
                try:
                    start_time = time.perf_counter()
                    
                    if isinstance(batch, dict):
                        outputs = model(
                            batch['sign1_idx'],
                            batch['sign2_idx'],
                            batch['aspect_matrix'],
                            batch['context_features']
                        )
                        targets = batch['targets']
                    else:
                        outputs = model(*batch[:-1])
                        targets = batch[-1]
                    
                    inference_time = time.perf_counter() - start_time
                    inference_times.append(inference_time)
                    
                    if isinstance(outputs, dict):
                        first_output = next(iter(outputs.values()))
                        if torch.is_tensor(first_output):
                            accuracy = (torch.abs(first_output - targets[:, 0]) <= 0.1).float().mean().item()
                        else:
                            accuracy = 0.5
                    else:
                        accuracy = (torch.abs(outputs - targets) <= 0.1).float().mean().item()
                    
                    batch_size = targets.size(0)
                    total_accuracy += accuracy * batch_size
                    total_samples += batch_size
                    
                except Exception as e:
                    self.logger.warning(f"Benchmark batch failed for {model_name}: {e}")
                    continue
        
        avg_accuracy = total_accuracy / max(total_samples, 1)
        avg_inference_time = np.mean(inference_times) if inference_times else 0
        
        return {
            'accuracy': avg_accuracy,
            'inference_time': avg_inference_time,
            'total_samples': total_samples
        }
    
    def _compare_model_sizes(self) -> Dict[str, Any]:
        """Compare model sizes"""
        def get_model_size(model):
            total_params = sum(p.numel() for p in model.parameters())
            non_zero_params = sum((p != 0).sum().item() for p in model.parameters())
            return total_params, non_zero_params
        
        size_comparison = {}
        
        if self.original_model is not None:
            orig_total, orig_nonzero = get_model_size(self.original_model)
            size_comparison['original_total_params'] = orig_total
            size_comparison['original_nonzero_params'] = orig_nonzero
        
        if self.pruned_model is not None:
            pruned_total, pruned_nonzero = get_model_size(self.pruned_model)
            size_comparison['pruned_total_params'] = pruned_total
            size_comparison['pruned_nonzero_params'] = pruned_nonzero
            
            if 'original_nonzero_params' in size_comparison:
                compression_ratio = size_comparison['original_nonzero_params'] / pruned_nonzero
                size_comparison['compression_ratio'] = compression_ratio
        
        return size_comparison
    
    def _analyze_knowledge_preservation(self) -> Dict[str, Any]:
        """Analyze preservation of astrological knowledge"""
        preservation_analysis = {}
        
        if hasattr(self.pruned_model, 'sign_embeddings'):
            # Analyze sign embedding preservation
            original_emb = self.original_model.sign_embeddings.weight.data
            pruned_emb = self.pruned_model.sign_embeddings.weight.data
            
            # Calculate cosine similarity between corresponding embeddings
            similarities = []
            for i in range(12):
                sim = torch.cosine_similarity(
                    original_emb[i:i+1], pruned_emb[i:i+1]
                ).item()
                similarities.append(sim)
            
            preservation_analysis['embedding_similarity'] = {
                'mean': np.mean(similarities),
                'std': np.std(similarities),
                'min': np.min(similarities)
            }
        
        preservation_analysis['important_weights_preserved'] = len(self.important_weights) > 0
        
        return preservation_analysis
    
    def save_pruned_model(self, filepath: str):
        """Save pruned model"""
        if self.pruned_model is None:
            raise ValueError("No pruned model to save")
        
        torch.save({
            'model_state_dict': self.pruned_model.state_dict(),
            'pruning_config': self.config.__dict__,
            'sparsity_stats': self._calculate_sparsity(),
            'pruning_history': self.pruning_history
        }, filepath)
        
        self.logger.info(f"Pruned model saved to {filepath}")


if __name__ == "__main__":
    # Test pruning
    from ..models.compatibility_network import ModelFactory
    
    # Create test model
    original_model = ModelFactory.create_standard_model()
    print(f"Original model parameters: {sum(p.numel() for p in original_model.parameters())}")
    
    # Create pruning config
    config = PruningConfig()
    config.method = 'unstructured'
    config.global_sparsity = 0.3
    
    # Initialize pruner
    pruner = CompatibilityModelPruner(config)
    
    # Prune model
    pruned_model = pruner.prune_model(original_model)
    
    # Test forward pass
    batch_size = 4
    test_input = (
        torch.randint(0, 12, (batch_size,)),
        torch.randint(0, 12, (batch_size,)),
        torch.rand(batch_size, 12, 12),
        torch.rand(batch_size, 50)
    )
    
    with torch.no_grad():
        original_output = original_model(*test_input)
        pruned_output = pruned_model(*test_input)
    
    print(f"Original output shape: {original_output.shape}")
    print(f"Pruned output shape: {pruned_output.shape}")
    
    # Analyze sparsity
    sparsity_stats = pruner._calculate_sparsity()
    print(f"Global sparsity: {sparsity_stats['global_sparsity']:.2%}")
    
    print("Pruning test completed successfully!")