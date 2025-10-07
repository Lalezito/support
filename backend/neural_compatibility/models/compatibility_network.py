import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Optional, Tuple
import time

class CompatibilityNeuralNetwork(nn.Module):
    """
    Advanced AI-Driven 12-Dimensional Compatibility Engine
    Hybrid transformer-CNN architecture with attention mechanisms
    
    Performance Targets:
    - Inference: <400ms
    - Accuracy: >98%
    - Memory: <200MB
    """
    
    def __init__(self, embedding_dim=512, num_dimensions=12, num_signs=12, num_aspects=144):
        super(CompatibilityNeuralNetwork, self).__init__()
        
        self.embedding_dim = embedding_dim
        self.num_dimensions = num_dimensions
        self.num_signs = num_signs
        
        # Sign embedding layer with learned representations
        self.sign_embeddings = nn.Embedding(num_signs, embedding_dim)
        self.aspect_embeddings = nn.Embedding(num_aspects, embedding_dim // 2)
        
        # Multi-head attention for zodiac relationships
        self.compatibility_attention = nn.MultiheadAttention(
            embed_dim=embedding_dim,
            num_heads=8,
            dropout=0.1,
            batch_first=True
        )
        
        # Transformer encoder for deep compatibility analysis
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embedding_dim,
            nhead=8,
            dim_feedforward=2048,
            dropout=0.1,
            activation='gelu',
            batch_first=True
        )
        self.transformer_layers = nn.TransformerEncoder(
            encoder_layer,
            num_layers=6
        )
        
        # CNN layers for pattern recognition in compatibility matrices
        self.conv_layers = nn.Sequential(
            nn.Conv2d(1, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(64),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(128),
            nn.AdaptiveAvgPool2d((8, 8))
        )
        
        # Context feature processing
        self.context_processor = nn.Sequential(
            nn.Linear(50, 256),  # Assuming 50 context features
            nn.ReLU(inplace=True),
            nn.Dropout(0.2),
            nn.Linear(256, 512)
        )
        
        # Final compatibility prediction layers
        combined_feature_dim = embedding_dim + 8192 + 512  # transformer + conv + context
        self.compatibility_head = nn.Sequential(
            nn.Linear(combined_feature_dim, 1024),
            nn.ReLU(inplace=True),
            nn.Dropout(0.2),
            nn.Linear(1024, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.1),
            nn.Linear(256, num_dimensions),
            nn.Sigmoid()
        )
        
        # Initialize weights
        self._initialize_weights()
        
    def _initialize_weights(self):
        """Initialize model weights using Xavier/Kaiming initialization"""
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.kaiming_normal_(module.weight, mode='fan_out', nonlinearity='relu')
                if module.bias is not None:
                    nn.init.constant_(module.bias, 0)
            elif isinstance(module, nn.Embedding):
                nn.init.xavier_uniform_(module.weight)
            elif isinstance(module, nn.Conv2d):
                nn.init.kaiming_normal_(module.weight, mode='fan_out', nonlinearity='relu')
                if module.bias is not None:
                    nn.init.constant_(module.bias, 0)
            elif isinstance(module, nn.BatchNorm2d):
                nn.init.constant_(module.weight, 1)
                nn.init.constant_(module.bias, 0)
    
    def forward(self, sign1_idx: torch.Tensor, sign2_idx: torch.Tensor, 
                aspect_matrix: torch.Tensor, context_features: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through the neural network
        
        Args:
            sign1_idx: Batch of first zodiac sign indices [batch_size]
            sign2_idx: Batch of second zodiac sign indices [batch_size] 
            aspect_matrix: Compatibility matrices [batch_size, 12, 12]
            context_features: Additional context features [batch_size, 50]
            
        Returns:
            Compatibility scores for 12 dimensions [batch_size, 12]
        """
        batch_size = sign1_idx.size(0)
        
        # Generate embeddings
        sign1_emb = self.sign_embeddings(sign1_idx)  # [batch_size, embedding_dim]
        sign2_emb = self.sign_embeddings(sign2_idx)  # [batch_size, embedding_dim]
        
        # Create sequence for transformer processing
        sign_sequence = torch.stack([sign1_emb, sign2_emb], dim=1)  # [batch_size, 2, embedding_dim]
        
        # Apply attention mechanism
        attended_features, attention_weights = self.compatibility_attention(
            sign_sequence, sign_sequence, sign_sequence
        )
        
        # Process through transformer
        transformed_features = self.transformer_layers(attended_features)
        
        # Global average pooling for transformer features
        transformer_output = torch.mean(transformed_features, dim=1)  # [batch_size, embedding_dim]
        
        # CNN processing of aspect matrix
        if len(aspect_matrix.shape) == 3:
            aspect_matrix = aspect_matrix.unsqueeze(1)  # Add channel dimension
            
        aspect_features = self.conv_layers(aspect_matrix)  # [batch_size, 128, 8, 8]
        aspect_features = aspect_features.flatten(start_dim=1)  # [batch_size, 8192]
        
        # Process context features
        context_processed = self.context_processor(context_features)  # [batch_size, 512]
        
        # Combine all features
        combined_features = torch.cat([
            transformer_output,
            aspect_features,
            context_processed
        ], dim=-1)
        
        # Generate compatibility scores
        compatibility_scores = self.compatibility_head(combined_features)
        
        return compatibility_scores
    
    def get_attention_weights(self, sign1_idx: torch.Tensor, sign2_idx: torch.Tensor) -> torch.Tensor:
        """Extract attention weights for interpretability"""
        with torch.no_grad():
            sign1_emb = self.sign_embeddings(sign1_idx)
            sign2_emb = self.sign_embeddings(sign2_idx)
            sign_sequence = torch.stack([sign1_emb, sign2_emb], dim=1)
            
            _, attention_weights = self.compatibility_attention(
                sign_sequence, sign_sequence, sign_sequence
            )
            
        return attention_weights
    
    def predict_batch(self, batch_data: dict) -> Tuple[torch.Tensor, float]:
        """
        Optimized batch prediction with timing
        
        Returns:
            Tuple of (predictions, inference_time_ms)
        """
        start_time = time.perf_counter()
        
        with torch.no_grad():
            self.eval()
            predictions = self.forward(
                batch_data['sign1_idx'],
                batch_data['sign2_idx'], 
                batch_data['aspect_matrix'],
                batch_data['context_features']
            )
        
        inference_time = (time.perf_counter() - start_time) * 1000  # Convert to ms
        
        return predictions, inference_time
    
    def get_model_info(self) -> dict:
        """Get model architecture information"""
        total_params = sum(p.numel() for p in self.parameters())
        trainable_params = sum(p.numel() for p in self.parameters() if p.requires_grad)
        
        return {
            'total_parameters': total_params,
            'trainable_parameters': trainable_params,
            'embedding_dim': self.embedding_dim,
            'num_dimensions': self.num_dimensions,
            'model_size_mb': total_params * 4 / 1024 / 1024  # Assuming float32
        }


class CompatibilityEmbeddings(nn.Module):
    """Advanced embedding layer for zodiac signs and aspects"""
    
    def __init__(self, num_signs=12, num_aspects=144, embedding_dim=512):
        super().__init__()
        
        self.sign_embeddings = nn.Embedding(num_signs, embedding_dim)
        self.aspect_embeddings = nn.Embedding(num_aspects, embedding_dim // 2)
        
        # Positional encodings for temporal aspects
        self.positional_encoding = self._create_positional_encoding(embedding_dim)
        
        # Element and modality embeddings
        self.element_embeddings = nn.Embedding(4, embedding_dim // 4)  # Fire, Earth, Air, Water
        self.modality_embeddings = nn.Embedding(3, embedding_dim // 4)  # Cardinal, Fixed, Mutable
        
    def _create_positional_encoding(self, d_model: int, max_len: int = 5000) -> torch.Tensor:
        """Create sinusoidal positional encodings"""
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * 
                           (-np.log(10000.0) / d_model))
        
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        
        return pe
    
    def forward(self, sign_indices: torch.Tensor, temporal_position: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        Forward pass for enhanced embeddings
        
        Args:
            sign_indices: Zodiac sign indices [batch_size]
            temporal_position: Optional temporal position for time-based compatibility
            
        Returns:
            Enhanced embeddings [batch_size, embedding_dim]
        """
        # Basic sign embeddings
        embeddings = self.sign_embeddings(sign_indices)
        
        # Add positional encoding if temporal position provided
        if temporal_position is not None:
            pos_enc = self.positional_encoding[temporal_position]
            embeddings = embeddings + pos_enc
        
        return embeddings


# Model factory for different configurations
class ModelFactory:
    """Factory class for creating different model configurations"""
    
    @staticmethod
    def create_lightweight_model() -> CompatibilityNeuralNetwork:
        """Create lightweight model for mobile deployment"""
        return CompatibilityNeuralNetwork(
            embedding_dim=256,
            num_dimensions=12
        )
    
    @staticmethod
    def create_standard_model() -> CompatibilityNeuralNetwork:
        """Create standard model for server deployment"""
        return CompatibilityNeuralNetwork(
            embedding_dim=512,
            num_dimensions=12
        )
    
    @staticmethod
    def create_high_accuracy_model() -> CompatibilityNeuralNetwork:
        """Create high accuracy model for research"""
        return CompatibilityNeuralNetwork(
            embedding_dim=768,
            num_dimensions=12
        )


if __name__ == "__main__":
    # Test model creation and basic functionality
    model = ModelFactory.create_standard_model()
    print(f"Model created with {model.get_model_info()}")
    
    # Test forward pass
    batch_size = 4
    sign1 = torch.randint(0, 12, (batch_size,))
    sign2 = torch.randint(0, 12, (batch_size,))
    aspect_matrix = torch.rand(batch_size, 12, 12)
    context = torch.rand(batch_size, 50)
    
    with torch.no_grad():
        output = model(sign1, sign2, aspect_matrix, context)
        print(f"Output shape: {output.shape}")
        print(f"Sample compatibility scores: {output[0]}")