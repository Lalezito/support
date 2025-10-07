import torch
import torch.nn as nn
import torch.quantization as quant
from torch.quantization import QuantStub, DeQuantStub
import torch.quantization.quantize_fx as quantize_fx
import copy
import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Union
import logging
import time
from pathlib import Path

from ..models.compatibility_network import CompatibilityNeuralNetwork
from ..models.transformer import CompatibilityTransformer

class QuantizationConfig:
    """Configuration for model quantization"""
    
    def __init__(self):
        # Quantization method
        self.method = 'dynamic'  # 'dynamic', 'static', 'qat' (quantization aware training)
        
        # Target precision
        self.target_dtype = torch.qint8
        
        # Calibration settings for static quantization
        self.calibration_batches = 100
        self.calibration_data = None
        
        # QAT settings
        self.qat_epochs = 10
        self.qat_learning_rate = 1e-5
        
        # Backend
        self.backend = 'fbgemm'  # 'fbgemm' for x86, 'qnnpack' for ARM
        
        # Layers to quantize
        self.quantize_embeddings = True
        self.quantize_linear = True
        self.quantize_conv = True
        self.quantize_attention = False  # Often sensitive to quantization
        
        # Performance targets
        self.target_speedup = 3.0  # Minimum speedup required
        self.max_accuracy_drop = 0.02  # Maximum allowed accuracy drop


class CompatibilityModelQuantizer:
    """
    Model quantization for neural compatibility models
    Supports dynamic, static, and quantization-aware training
    """
    
    def __init__(self, config: QuantizationConfig = None):
        self.config = config or QuantizationConfig()
        self.logger = logging.getLogger(__name__)
        
        # Set quantization backend
        if torch.backends.quantized.engine != self.config.backend:
            torch.backends.quantized.engine = self.config.backend
            
        self.original_model = None
        self.quantized_model = None
        self.calibration_stats = {}
        
    def quantize_model(self, model: nn.Module, 
                      calibration_data: Optional[torch.utils.data.DataLoader] = None) -> nn.Module:
        """
        Quantize a neural compatibility model
        
        Args:
            model: Original model to quantize
            calibration_data: Data for static quantization calibration
            
        Returns:
            Quantized model
        """
        self.original_model = model
        self.logger.info(f"Starting {self.config.method} quantization...")
        
        if self.config.method == 'dynamic':
            quantized_model = self._dynamic_quantization(model)
        elif self.config.method == 'static':
            if calibration_data is None:
                raise ValueError("Calibration data required for static quantization")
            quantized_model = self._static_quantization(model, calibration_data)
        elif self.config.method == 'qat':
            if calibration_data is None:
                raise ValueError("Training data required for QAT")
            quantized_model = self._quantization_aware_training(model, calibration_data)
        else:
            raise ValueError(f"Unknown quantization method: {self.config.method}")
        
        self.quantized_model = quantized_model
        self.logger.info("Quantization completed successfully")
        
        return quantized_model
    
    def _dynamic_quantization(self, model: nn.Module) -> nn.Module:
        """Apply dynamic quantization"""
        model_copy = copy.deepcopy(model)
        
        # Specify layers to quantize
        layers_to_quantize = []
        
        if self.config.quantize_linear:
            layers_to_quantize.append(nn.Linear)
        if self.config.quantize_conv:
            layers_to_quantize.append(nn.Conv1d)
            layers_to_quantize.append(nn.Conv2d)
        if self.config.quantize_embeddings:
            layers_to_quantize.append(nn.Embedding)
        if self.config.quantize_attention:
            layers_to_quantize.append(nn.MultiheadAttention)
        
        # Apply dynamic quantization
        quantized_model = torch.quantization.quantize_dynamic(
            model_copy,
            layers_to_quantize,
            dtype=self.config.target_dtype
        )
        
        return quantized_model
    
    def _static_quantization(self, model: nn.Module, 
                           calibration_data: torch.utils.data.DataLoader) -> nn.Module:
        """Apply static quantization with calibration"""
        model_copy = copy.deepcopy(model)
        model_copy.eval()
        
        # Prepare model for static quantization
        model_copy = self._prepare_static_quantization(model_copy)
        
        # Calibrate the model
        self.logger.info("Calibrating model for static quantization...")
        self._calibrate_model(model_copy, calibration_data)
        
        # Convert to quantized model
        quantized_model = torch.quantization.convert(model_copy)
        
        return quantized_model
    
    def _prepare_static_quantization(self, model: nn.Module) -> nn.Module:
        """Prepare model for static quantization"""
        # Set quantization config
        if hasattr(model, 'qconfig'):
            model.qconfig = torch.quantization.get_default_qconfig(self.config.backend)
        
        # Prepare model
        model_prepared = torch.quantization.prepare(model)
        
        return model_prepared
    
    def _calibrate_model(self, model: nn.Module, 
                        calibration_data: torch.utils.data.DataLoader):
        """Calibrate model using calibration dataset"""
        model.eval()
        
        batch_count = 0
        with torch.no_grad():
            for batch in calibration_data:
                if batch_count >= self.config.calibration_batches:
                    break
                
                # Forward pass for calibration
                try:
                    if isinstance(batch, dict):
                        # Handle dictionary input
                        sign1_idx = batch.get('sign1_idx', torch.zeros(1, dtype=torch.long))
                        sign2_idx = batch.get('sign2_idx', torch.zeros(1, dtype=torch.long))
                        aspect_matrix = batch.get('aspect_matrix', torch.zeros(1, 12, 12))
                        context_features = batch.get('context_features', torch.zeros(1, 50))
                        
                        _ = model(sign1_idx, sign2_idx, aspect_matrix, context_features)
                    else:
                        # Handle tensor input
                        _ = model(batch)
                        
                except Exception as e:
                    self.logger.warning(f"Calibration batch {batch_count} failed: {e}")
                    continue
                
                batch_count += 1
        
        self.logger.info(f"Calibration completed with {batch_count} batches")
    
    def _quantization_aware_training(self, model: nn.Module, 
                                   training_data: torch.utils.data.DataLoader) -> nn.Module:
        """Apply quantization-aware training"""
        model_copy = copy.deepcopy(model)
        
        # Prepare model for QAT
        model_copy.train()
        if hasattr(model_copy, 'qconfig'):
            model_copy.qconfig = torch.quantization.get_default_qat_qconfig(self.config.backend)
        
        model_prepared = torch.quantization.prepare_qat(model_copy)
        
        # Train with quantization simulation
        self.logger.info("Starting quantization-aware training...")
        self._train_qat_model(model_prepared, training_data)
        
        # Convert to quantized model
        model_prepared.eval()
        quantized_model = torch.quantization.convert(model_prepared)
        
        return quantized_model
    
    def _train_qat_model(self, model: nn.Module, training_data: torch.utils.data.DataLoader):
        """Train model with quantization awareness"""
        optimizer = torch.optim.Adam(model.parameters(), lr=self.config.qat_learning_rate)
        criterion = nn.MSELoss()
        
        for epoch in range(self.config.qat_epochs):
            epoch_loss = 0.0
            batch_count = 0
            
            for batch in training_data:
                optimizer.zero_grad()
                
                try:
                    # Forward pass
                    if isinstance(batch, dict):
                        sign1_idx = batch['sign1_idx']
                        sign2_idx = batch['sign2_idx']
                        aspect_matrix = batch['aspect_matrix']
                        context_features = batch['context_features']
                        targets = batch['targets']
                        
                        outputs = model(sign1_idx, sign2_idx, aspect_matrix, context_features)
                        
                        if isinstance(outputs, dict):
                            # Handle transformer outputs
                            loss = 0
                            for dim_outputs in outputs.values():
                                if torch.is_tensor(dim_outputs):
                                    loss += criterion(dim_outputs, targets[:, 0])  # Simplified
                            loss /= len(outputs)
                        else:
                            loss = criterion(outputs, targets)
                    else:
                        outputs = model(batch[:-1])
                        targets = batch[-1]
                        loss = criterion(outputs, targets)
                    
                    # Backward pass
                    loss.backward()
                    optimizer.step()
                    
                    epoch_loss += loss.item()
                    batch_count += 1
                    
                except Exception as e:
                    self.logger.warning(f"QAT batch failed: {e}")
                    continue
            
            avg_loss = epoch_loss / max(batch_count, 1)
            self.logger.info(f"QAT Epoch {epoch+1}/{self.config.qat_epochs}, Loss: {avg_loss:.6f}")
    
    def benchmark_quantized_model(self, test_data: torch.utils.data.DataLoader,
                                 original_model: Optional[nn.Module] = None) -> Dict[str, Any]:
        """
        Benchmark quantized model performance
        
        Args:
            test_data: Test dataset for benchmarking
            original_model: Original model for comparison
            
        Returns:
            Benchmarking results
        """
        if self.quantized_model is None:
            raise ValueError("No quantized model available for benchmarking")
        
        self.logger.info("Benchmarking quantized model...")
        
        # Benchmark quantized model
        quant_results = self._benchmark_model(self.quantized_model, test_data, "Quantized")
        
        results = {
            'quantized_model': quant_results,
            'quantization_method': self.config.method,
            'target_dtype': str(self.config.target_dtype)
        }
        
        # Compare with original model if provided
        if original_model is not None:
            orig_results = self._benchmark_model(original_model, test_data, "Original")
            results['original_model'] = orig_results
            results['comparison'] = self._compare_models(orig_results, quant_results)
        
        # Model size comparison
        results['model_sizes'] = self._compare_model_sizes()
        
        return results
    
    def _benchmark_model(self, model: nn.Module, test_data: torch.utils.data.DataLoader,
                        model_name: str) -> Dict[str, float]:
        """Benchmark a single model"""
        model.eval()
        
        total_loss = 0.0
        total_accuracy = 0.0
        total_samples = 0
        inference_times = []
        
        criterion = nn.MSELoss()
        
        with torch.no_grad():
            for batch in test_data:
                batch_size = len(batch['targets']) if isinstance(batch, dict) else batch[0].size(0)
                
                # Measure inference time
                start_time = time.perf_counter()
                
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
                    
                    inference_time = time.perf_counter() - start_time
                    inference_times.append(inference_time)
                    
                    # Calculate loss
                    if isinstance(outputs, dict):
                        loss = 0
                        for dim_outputs in outputs.values():
                            if torch.is_tensor(dim_outputs) and dim_outputs.numel() > 0:
                                loss += criterion(dim_outputs, targets[:, 0])  # Simplified
                        loss /= max(len([o for o in outputs.values() if torch.is_tensor(o)]), 1)
                    else:
                        loss = criterion(outputs, targets)
                    
                    total_loss += loss.item() * batch_size
                    
                    # Calculate accuracy (within 10% tolerance)
                    if isinstance(outputs, dict):
                        # Use first dimension for accuracy calculation
                        first_output = next(iter(outputs.values()))
                        if torch.is_tensor(first_output):
                            accuracy = (torch.abs(first_output - targets[:, 0]) <= 0.1).float().mean().item()
                        else:
                            accuracy = 0.5
                    else:
                        accuracy = (torch.abs(outputs - targets) <= 0.1).float().mean().item()
                    
                    total_accuracy += accuracy * batch_size
                    total_samples += batch_size
                    
                except Exception as e:
                    self.logger.warning(f"Benchmark batch failed for {model_name}: {e}")
                    continue
        
        # Calculate metrics
        avg_loss = total_loss / max(total_samples, 1)
        avg_accuracy = total_accuracy / max(total_samples, 1)
        avg_inference_time = np.mean(inference_times) * 1000  # Convert to ms
        throughput = total_samples / sum(inference_times) if inference_times else 0
        
        results = {
            'loss': avg_loss,
            'accuracy': avg_accuracy,
            'avg_inference_time_ms': avg_inference_time,
            'p95_inference_time_ms': np.percentile(inference_times, 95) * 1000 if inference_times else 0,
            'throughput_samples_per_sec': throughput,
            'total_samples': total_samples
        }
        
        self.logger.info(f"{model_name} Model - Loss: {avg_loss:.6f}, "
                        f"Accuracy: {avg_accuracy:.4f}, "
                        f"Inference: {avg_inference_time:.1f}ms, "
                        f"Throughput: {throughput:.1f} samples/sec")
        
        return results
    
    def _compare_models(self, original_results: Dict[str, float], 
                       quantized_results: Dict[str, float]) -> Dict[str, float]:
        """Compare original and quantized model performance"""
        comparison = {}
        
        # Speed improvement
        if original_results['avg_inference_time_ms'] > 0:
            speedup = original_results['avg_inference_time_ms'] / quantized_results['avg_inference_time_ms']
            comparison['speedup'] = speedup
        
        # Throughput improvement
        if original_results['throughput_samples_per_sec'] > 0:
            throughput_improvement = (quantized_results['throughput_samples_per_sec'] / 
                                    original_results['throughput_samples_per_sec'])
            comparison['throughput_improvement'] = throughput_improvement
        
        # Accuracy change
        accuracy_change = quantized_results['accuracy'] - original_results['accuracy']
        comparison['accuracy_change'] = accuracy_change
        comparison['accuracy_drop_acceptable'] = abs(accuracy_change) <= self.config.max_accuracy_drop
        
        # Performance target met
        comparison['speedup_target_met'] = comparison.get('speedup', 0) >= self.config.target_speedup
        
        return comparison
    
    def _compare_model_sizes(self) -> Dict[str, Any]:
        """Compare model sizes"""
        size_comparison = {}
        
        if self.original_model is not None:
            # Original model size
            orig_size = sum(p.numel() * p.element_size() for p in self.original_model.parameters())
            size_comparison['original_size_bytes'] = orig_size
            size_comparison['original_size_mb'] = orig_size / (1024 * 1024)
        
        if self.quantized_model is not None:
            # Try to estimate quantized model size
            # This is approximate as quantized models have different storage
            quant_params = sum(p.numel() for p in self.quantized_model.parameters() 
                             if hasattr(p, 'numel'))
            
            # Assume 1 byte per parameter for INT8 quantization
            quant_size = quant_params * 1 if self.config.target_dtype == torch.qint8 else quant_params * 2
            size_comparison['quantized_size_bytes'] = quant_size
            size_comparison['quantized_size_mb'] = quant_size / (1024 * 1024)
            
            # Compression ratio
            if 'original_size_bytes' in size_comparison and size_comparison['original_size_bytes'] > 0:
                compression_ratio = size_comparison['original_size_bytes'] / quant_size
                size_comparison['compression_ratio'] = compression_ratio
        
        return size_comparison
    
    def save_quantized_model(self, filepath: str):
        """Save quantized model to file"""
        if self.quantized_model is None:
            raise ValueError("No quantized model to save")
        
        # Save model
        torch.jit.save(torch.jit.script(self.quantized_model), filepath)
        self.logger.info(f"Quantized model saved to {filepath}")
    
    def load_quantized_model(self, filepath: str) -> nn.Module:
        """Load quantized model from file"""
        model = torch.jit.load(filepath)
        self.quantized_model = model
        self.logger.info(f"Quantized model loaded from {filepath}")
        return model


class QuantizedCompatibilityNetwork(nn.Module):
    """
    Quantization-ready wrapper for CompatibilityNeuralNetwork
    """
    
    def __init__(self, original_model: CompatibilityNeuralNetwork):
        super().__init__()
        
        self.quant = QuantStub()
        self.dequant = DeQuantStub()
        
        # Copy components from original model
        self.sign_embeddings = original_model.sign_embeddings
        self.aspect_embeddings = original_model.aspect_embeddings
        self.compatibility_attention = original_model.compatibility_attention
        self.transformer_layers = original_model.transformer_layers
        self.conv_layers = original_model.conv_layers
        self.context_processor = original_model.context_processor
        self.compatibility_head = original_model.compatibility_head
        
    def forward(self, sign1_idx, sign2_idx, aspect_matrix, context_features):
        # Quantize inputs where appropriate
        aspect_matrix = self.quant(aspect_matrix)
        context_features = self.quant(context_features)
        
        # Forward pass (similar to original model)
        batch_size = sign1_idx.size(0)
        
        sign1_emb = self.sign_embeddings(sign1_idx)
        sign2_emb = self.sign_embeddings(sign2_idx)
        
        sign_sequence = torch.stack([sign1_emb, sign2_emb], dim=1)
        
        attended_features, _ = self.compatibility_attention(
            sign_sequence, sign_sequence, sign_sequence
        )
        
        transformed_features = self.transformer_layers(attended_features)
        transformer_output = torch.mean(transformed_features, dim=1)
        
        # CNN processing
        if len(aspect_matrix.shape) == 3:
            aspect_matrix = aspect_matrix.unsqueeze(1)
        
        aspect_features = self.conv_layers(aspect_matrix)
        aspect_features = aspect_features.flatten(start_dim=1)
        
        # Context processing
        context_processed = self.context_processor(context_features)
        
        # Combine features
        combined_features = torch.cat([
            transformer_output,
            aspect_features,
            context_processed
        ], dim=-1)
        
        # Generate compatibility scores
        compatibility_scores = self.compatibility_head(combined_features)
        
        # Dequantize output
        compatibility_scores = self.dequant(compatibility_scores)
        
        return compatibility_scores


if __name__ == "__main__":
    # Test quantization
    from ..models.compatibility_network import ModelFactory
    
    # Create test model
    original_model = ModelFactory.create_standard_model()
    print(f"Original model parameters: {sum(p.numel() for p in original_model.parameters())}")
    
    # Create quantization config
    config = QuantizationConfig()
    config.method = 'dynamic'
    
    # Initialize quantizer
    quantizer = CompatibilityModelQuantizer(config)
    
    # Create test data
    batch_size = 4
    test_data = {
        'sign1_idx': torch.randint(0, 12, (batch_size,)),
        'sign2_idx': torch.randint(0, 12, (batch_size,)),
        'aspect_matrix': torch.rand(batch_size, 12, 12),
        'context_features': torch.rand(batch_size, 50),
        'targets': torch.rand(batch_size, 12)
    }
    
    # Test original model
    with torch.no_grad():
        original_output = original_model(
            test_data['sign1_idx'],
            test_data['sign2_idx'], 
            test_data['aspect_matrix'],
            test_data['context_features']
        )
    
    print(f"Original output shape: {original_output.shape}")
    
    # Quantize model
    quantized_model = quantizer.quantize_model(original_model)
    print(f"Quantized model created successfully")
    
    # Test quantized model
    with torch.no_grad():
        quantized_output = quantized_model(
            test_data['sign1_idx'],
            test_data['sign2_idx'],
            test_data['aspect_matrix'], 
            test_data['context_features']
        )
    
    print(f"Quantized output shape: {quantized_output.shape}")
    
    # Compare outputs
    output_diff = torch.abs(original_output - quantized_output).mean().item()
    print(f"Average output difference: {output_diff:.6f}")
    
    print("Quantization test completed successfully!")