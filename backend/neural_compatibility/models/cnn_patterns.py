import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Tuple, List, Optional, Dict

class CompatibilityMatrixCNN(nn.Module):
    """
    CNN for pattern recognition in zodiac compatibility matrices
    Detects astrological patterns and relationships in 2D compatibility data
    """
    
    def __init__(self, input_channels: int = 1, output_features: int = 512):
        super().__init__()
        
        self.input_channels = input_channels
        self.output_features = output_features
        
        # Multi-scale convolutional layers for different pattern sizes
        self.conv_blocks = nn.ModuleList([
            self._make_conv_block(input_channels, 64, kernel_size=3, padding=1),   # Fine patterns
            self._make_conv_block(64, 128, kernel_size=5, padding=2),              # Medium patterns
            self._make_conv_block(128, 256, kernel_size=7, padding=3),             # Large patterns
        ])
        
        # Attention-guided feature extraction
        self.attention_conv = nn.Conv2d(256, 256, kernel_size=1)
        self.attention_pool = nn.AdaptiveAvgPool2d(1)
        
        # Spatial attention mechanism
        self.spatial_attention = SpatialAttention()
        
        # Channel attention mechanism  
        self.channel_attention = ChannelAttention(256)
        
        # Global feature extraction
        self.global_pool = nn.AdaptiveAvgPool2d((4, 4))
        
        # Final feature projection
        self.feature_projection = nn.Sequential(
            nn.Linear(256 * 4 * 4, 1024),
            nn.ReLU(inplace=True),
            nn.Dropout(0.2),
            nn.Linear(1024, output_features),
            nn.ReLU(inplace=True)
        )
        
    def _make_conv_block(self, in_channels: int, out_channels: int, 
                        kernel_size: int, padding: int) -> nn.Module:
        """Create a convolutional block with batch norm and activation"""
        return nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size, 
                     padding=padding, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=kernel_size,
                     padding=padding, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
    
    def forward(self, compatibility_matrices: torch.Tensor) -> torch.Tensor:
        """
        Extract features from compatibility matrices
        
        Args:
            compatibility_matrices: Input matrices [batch_size, channels, height, width]
            
        Returns:
            Extracted features [batch_size, output_features]
        """
        x = compatibility_matrices
        
        # Apply multi-scale convolutions
        for conv_block in self.conv_blocks:
            x = conv_block(x)
        
        # Apply attention mechanisms
        x = self.channel_attention(x)
        x = self.spatial_attention(x)
        
        # Global pooling
        x = self.global_pool(x)
        
        # Flatten and project to output features
        x = x.view(x.size(0), -1)
        features = self.feature_projection(x)
        
        return features


class AstrologicalPatternDetector(nn.Module):
    """
    Specialized CNN for detecting specific astrological patterns in compatibility matrices
    """
    
    def __init__(self, matrix_size: int = 12):
        super().__init__()
        
        self.matrix_size = matrix_size
        
        # Pattern-specific filters
        self.element_pattern_conv = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.modality_pattern_conv = nn.Conv2d(1, 16, kernel_size=3, padding=1) 
        self.aspect_pattern_conv = nn.Conv2d(1, 16, kernel_size=5, padding=2)
        self.house_pattern_conv = nn.Conv2d(1, 16, kernel_size=7, padding=3)
        
        # Initialize filters with astrological knowledge
        self._initialize_astrological_filters()
        
        # Feature combination
        self.pattern_combination = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(128),
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(256)
        )
        
        # Pattern strength estimation
        self.pattern_strength = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 12)  # Strength for each astrological dimension
        )
        
    def _initialize_astrological_filters(self):
        """Initialize CNN filters with astrological pattern knowledge"""
        with torch.no_grad():
            # Element compatibility patterns (Fire, Earth, Air, Water)
            element_pattern = self._create_element_pattern()
            self.element_pattern_conv.weight[0, 0] = element_pattern
            
            # Modality patterns (Cardinal, Fixed, Mutable)  
            modality_pattern = self._create_modality_pattern()
            self.modality_pattern_conv.weight[0, 0] = modality_pattern
            
            # Aspect angle patterns
            aspect_pattern = self._create_aspect_pattern()
            if aspect_pattern.size() == self.aspect_pattern_conv.weight[0, 0].size():
                self.aspect_pattern_conv.weight[0, 0] = aspect_pattern
    
    def _create_element_pattern(self) -> torch.Tensor:
        """Create element compatibility pattern"""
        pattern = torch.zeros(3, 3)
        # Fire-Air and Earth-Water harmonies
        pattern[0, 2] = 1.0  # Fire-Air
        pattern[1, 3] = 1.0  # Earth-Water (adjusted for 3x3)
        pattern[2, 0] = 1.0  # Air-Fire
        return pattern
    
    def _create_modality_pattern(self) -> torch.Tensor:
        """Create modality pattern (Cardinal, Fixed, Mutable)"""
        pattern = torch.zeros(3, 3)
        # Cardinal square pattern
        pattern[0, 0] = 1.0
        pattern[1, 1] = 1.0  # Fixed
        pattern[2, 2] = 1.0  # Mutable
        return pattern
    
    def _create_aspect_pattern(self) -> torch.Tensor:
        """Create aspect angle pattern for major aspects"""
        pattern = torch.zeros(5, 5)
        center = 2
        
        # Trine pattern (120 degrees)
        pattern[center, center] = 1.0
        pattern[center-2, center] = 0.8
        pattern[center+2, center] = 0.8
        pattern[center, center-2] = 0.8
        pattern[center, center+2] = 0.8
        
        return pattern
    
    def forward(self, compatibility_matrix: torch.Tensor) -> Dict[str, torch.Tensor]:
        """
        Detect astrological patterns in compatibility matrix
        
        Args:
            compatibility_matrix: Input matrix [batch_size, 1, height, width]
            
        Returns:
            Dictionary of detected patterns and strengths
        """
        # Apply pattern-specific convolutions
        element_features = F.relu(self.element_pattern_conv(compatibility_matrix))
        modality_features = F.relu(self.modality_pattern_conv(compatibility_matrix))
        aspect_features = F.relu(self.aspect_pattern_conv(compatibility_matrix))
        house_features = F.relu(self.house_pattern_conv(compatibility_matrix))
        
        # Combine all pattern features
        combined_features = torch.cat([
            element_features, modality_features, aspect_features, house_features
        ], dim=1)
        
        # Process combined patterns
        pattern_features = self.pattern_combination(combined_features)
        
        # Estimate pattern strengths
        pattern_strengths = self.pattern_strength(pattern_features)
        
        return {
            'element_patterns': element_features,
            'modality_patterns': modality_features,
            'aspect_patterns': aspect_features,
            'house_patterns': house_features,
            'combined_features': pattern_features,
            'pattern_strengths': pattern_strengths
        }


class SpatialAttention(nn.Module):
    """
    Spatial attention mechanism for focusing on important regions
    """
    
    def __init__(self, kernel_size: int = 7):
        super().__init__()
        
        self.conv = nn.Conv2d(2, 1, kernel_size=kernel_size, padding=kernel_size//2, bias=False)
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Channel-wise statistics
        avg_pool = torch.mean(x, dim=1, keepdim=True)
        max_pool, _ = torch.max(x, dim=1, keepdim=True)
        
        # Concatenate and apply convolution
        spatial_features = torch.cat([avg_pool, max_pool], dim=1)
        attention_map = self.sigmoid(self.conv(spatial_features))
        
        return x * attention_map


class ChannelAttention(nn.Module):
    """
    Channel attention mechanism for feature recalibration
    """
    
    def __init__(self, channels: int, reduction_ratio: int = 16):
        super().__init__()
        
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.max_pool = nn.AdaptiveMaxPool2d(1)
        
        self.fc = nn.Sequential(
            nn.Linear(channels, channels // reduction_ratio, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(channels // reduction_ratio, channels, bias=False)
        )
        
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch_size, channels = x.size(0), x.size(1)
        
        # Global average pooling
        avg_pool = self.avg_pool(x).view(batch_size, channels)
        avg_weights = self.fc(avg_pool)
        
        # Global max pooling
        max_pool = self.max_pool(x).view(batch_size, channels)
        max_weights = self.fc(max_pool)
        
        # Combine weights
        attention_weights = self.sigmoid(avg_weights + max_weights)
        attention_weights = attention_weights.view(batch_size, channels, 1, 1)
        
        return x * attention_weights


class ResidualCompatibilityBlock(nn.Module):
    """
    Residual block for deep compatibility pattern extraction
    """
    
    def __init__(self, channels: int):
        super().__init__()
        
        self.conv1 = nn.Conv2d(channels, channels, kernel_size=3, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(channels)
        self.conv2 = nn.Conv2d(channels, channels, kernel_size=3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(channels)
        
        self.relu = nn.ReLU(inplace=True)
        
        # SE block for channel recalibration
        self.se_block = ChannelAttention(channels)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        identity = x
        
        # First convolution
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        
        # Second convolution
        out = self.conv2(out)
        out = self.bn2(out)
        
        # SE attention
        out = self.se_block(out)
        
        # Residual connection
        out += identity
        out = self.relu(out)
        
        return out


class DeepCompatibilityNet(nn.Module):
    """
    Deep CNN for comprehensive compatibility pattern analysis
    """
    
    def __init__(self, input_size: int = 12, num_classes: int = 12):
        super().__init__()
        
        # Initial feature extraction
        self.initial_conv = nn.Sequential(
            nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        )
        
        # Residual blocks for deep feature extraction
        self.res_blocks = nn.Sequential(
            ResidualCompatibilityBlock(64),
            ResidualCompatibilityBlock(64),
            self._make_layer(64, 128, 2),
            ResidualCompatibilityBlock(128),
            ResidualCompatibilityBlock(128),
            self._make_layer(128, 256, 2),
            ResidualCompatibilityBlock(256),
            ResidualCompatibilityBlock(256),
        )
        
        # Astrological pattern detector
        self.pattern_detector = AstrologicalPatternDetector()
        
        # Feature fusion
        self.feature_fusion = nn.Sequential(
            nn.Conv2d(256 + 256, 512, kernel_size=1),  # CNN + Pattern features
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(512),
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten()
        )
        
        # Classification heads for compatibility dimensions
        self.compatibility_classifier = nn.Sequential(
            nn.Linear(512, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.2),
            nn.Linear(256, num_classes),
            nn.Sigmoid()
        )
        
    def _make_layer(self, in_channels: int, out_channels: int, stride: int) -> nn.Module:
        """Create transition layer between different feature map sizes"""
        return nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )
        
    def forward(self, compatibility_matrix: torch.Tensor) -> Dict[str, torch.Tensor]:
        """
        Comprehensive compatibility analysis
        
        Args:
            compatibility_matrix: Input matrix [batch_size, 1, height, width]
            
        Returns:
            Dictionary of compatibility scores and detected patterns
        """
        # Initial feature extraction
        cnn_features = self.initial_conv(compatibility_matrix)
        
        # Deep residual processing
        cnn_features = self.res_blocks(cnn_features)
        
        # Detect astrological patterns
        pattern_results = self.pattern_detector(compatibility_matrix)
        pattern_features = pattern_results['combined_features']
        
        # Resize pattern features to match CNN features
        if pattern_features.size(2) != cnn_features.size(2):
            pattern_features = F.interpolate(
                pattern_features, 
                size=(cnn_features.size(2), cnn_features.size(3)),
                mode='bilinear',
                align_corners=False
            )
        
        # Fuse CNN and pattern features
        fused_features = torch.cat([cnn_features, pattern_features], dim=1)
        final_features = self.feature_fusion(fused_features)
        
        # Generate compatibility scores
        compatibility_scores = self.compatibility_classifier(final_features)
        
        return {
            'compatibility_scores': compatibility_scores,
            'pattern_strengths': pattern_results['pattern_strengths'],
            'detected_patterns': pattern_results,
            'cnn_features': cnn_features,
            'fused_features': final_features
        }


class CompatibilityMatrixGenerator(nn.Module):
    """
    Generate compatibility matrices from zodiac sign pairs
    """
    
    def __init__(self, num_signs: int = 12, matrix_size: int = 12, embed_dim: int = 64):
        super().__init__()
        
        self.num_signs = num_signs
        self.matrix_size = matrix_size
        self.embed_dim = embed_dim
        
        # Sign embeddings
        self.sign_embeddings = nn.Embedding(num_signs, embed_dim)
        
        # Matrix generation network
        self.matrix_generator = nn.Sequential(
            nn.Linear(embed_dim * 2, 256),
            nn.ReLU(),
            nn.Linear(256, 512),
            nn.ReLU(),
            nn.Linear(512, matrix_size * matrix_size),
            nn.Sigmoid()
        )
        
        # Learnable compatibility templates
        self.compatibility_templates = nn.Parameter(
            torch.randn(num_signs, num_signs, matrix_size, matrix_size)
        )
        
    def forward(self, sign1_indices: torch.Tensor, sign2_indices: torch.Tensor) -> torch.Tensor:
        """
        Generate compatibility matrices for sign pairs
        
        Args:
            sign1_indices: First sign indices [batch_size]
            sign2_indices: Second sign indices [batch_size]
            
        Returns:
            Compatibility matrices [batch_size, 1, matrix_size, matrix_size]
        """
        batch_size = sign1_indices.size(0)
        
        # Get embeddings
        sign1_emb = self.sign_embeddings(sign1_indices)
        sign2_emb = self.sign_embeddings(sign2_indices)
        
        # Generate base matrices
        combined_emb = torch.cat([sign1_emb, sign2_emb], dim=-1)
        base_matrices = self.matrix_generator(combined_emb)
        base_matrices = base_matrices.view(batch_size, 1, self.matrix_size, self.matrix_size)
        
        # Add learnable templates
        template_matrices = torch.zeros_like(base_matrices)
        for i in range(batch_size):
            s1, s2 = sign1_indices[i].item(), sign2_indices[i].item()
            template_matrices[i, 0] = self.compatibility_templates[s1, s2]
        
        # Combine base and template matrices
        compatibility_matrices = 0.7 * base_matrices + 0.3 * template_matrices
        
        return compatibility_matrices


if __name__ == "__main__":
    # Test CNN components
    batch_size = 4
    matrix_size = 12
    
    # Test CompatibilityMatrixCNN
    cnn = CompatibilityMatrixCNN(input_channels=1, output_features=512)
    
    # Generate test compatibility matrices
    test_matrices = torch.randn(batch_size, 1, matrix_size, matrix_size)
    cnn_features = cnn(test_matrices)
    print(f"CNN features shape: {cnn_features.shape}")
    
    # Test AstrologicalPatternDetector
    pattern_detector = AstrologicalPatternDetector(matrix_size=matrix_size)
    pattern_results = pattern_detector(test_matrices)
    print(f"Pattern results keys: {list(pattern_results.keys())}")
    print(f"Pattern strengths shape: {pattern_results['pattern_strengths'].shape}")
    
    # Test DeepCompatibilityNet
    deep_net = DeepCompatibilityNet(input_size=matrix_size, num_classes=12)
    deep_results = deep_net(test_matrices)
    print(f"Deep net results keys: {list(deep_results.keys())}")
    print(f"Compatibility scores shape: {deep_results['compatibility_scores'].shape}")
    
    # Test CompatibilityMatrixGenerator
    matrix_generator = CompatibilityMatrixGenerator()
    sign1_indices = torch.tensor([0, 3, 6, 9])  # Aries, Cancer, Libra, Capricorn
    sign2_indices = torch.tensor([4, 7, 10, 1]) # Leo, Scorpio, Aquarius, Taurus
    
    generated_matrices = matrix_generator(sign1_indices, sign2_indices)
    print(f"Generated matrices shape: {generated_matrices.shape}")
    
    # Test complete pipeline
    pipeline_results = deep_net(generated_matrices)
    print(f"Pipeline compatibility scores: {pipeline_results['compatibility_scores']}")
    print(f"Pipeline pattern strengths: {pipeline_results['pattern_strengths']}")