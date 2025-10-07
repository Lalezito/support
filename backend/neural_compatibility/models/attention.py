import torch
import torch.nn as nn
import torch.nn.functional as F
import math
import numpy as np
from typing import Optional, Tuple

class AstrologicalAttention(nn.Module):
    """
    Specialized multi-head attention mechanism for astrological compatibility analysis
    Incorporates zodiac-specific attention patterns and interpretable weights
    """
    
    def __init__(self, embed_dim: int, num_heads: int = 8, dropout: float = 0.1):
        super().__init__()
        
        assert embed_dim % num_heads == 0, "embed_dim must be divisible by num_heads"
        
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        self.dropout = dropout
        
        # Query, Key, Value projections
        self.q_projection = nn.Linear(embed_dim, embed_dim, bias=False)
        self.k_projection = nn.Linear(embed_dim, embed_dim, bias=False)
        self.v_projection = nn.Linear(embed_dim, embed_dim, bias=False)
        
        # Output projection
        self.out_projection = nn.Linear(embed_dim, embed_dim)
        
        # Astrological knowledge integration
        self.zodiac_bias = nn.Parameter(torch.zeros(12, 12, num_heads))
        self.aspect_bias = nn.Parameter(torch.zeros(12, num_heads))  # Major aspects
        
        # Learnable temperature for attention sharpening
        self.temperature = nn.Parameter(torch.ones(num_heads))
        
        self.dropout_layer = nn.Dropout(dropout)
        
        self._initialize_astrological_biases()
    
    def _initialize_astrological_biases(self):
        """Initialize attention biases with astrological knowledge"""
        with torch.no_grad():
            # Element compatibility matrix
            element_compat = torch.tensor([
                [1.0, 0.3, 0.8, 0.3],  # Fire
                [0.3, 1.0, 0.3, 0.8],  # Earth
                [0.8, 0.3, 1.0, 0.3],  # Air  
                [0.3, 0.8, 0.3, 1.0]   # Water
            ])
            
            # Sign to element mapping
            sign_elements = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]
            
            # Initialize zodiac bias based on element compatibility
            for i in range(12):
                for j in range(12):
                    elem_i, elem_j = sign_elements[i], sign_elements[j]
                    compatibility = element_compat[elem_i, elem_j]
                    
                    # Apply bias across all attention heads
                    self.zodiac_bias[i, j] = compatibility * 0.1
            
            # Initialize aspect biases for major aspects
            aspect_strengths = [1.0, 0.8, 0.6, 0.4, 0.9, 0.2, 0.3, 0.5, 0.9, 0.4, 0.2, 0.1]
            for i, strength in enumerate(aspect_strengths):
                self.aspect_bias[i] = strength * 0.05
    
    def forward(self, query: torch.Tensor, key: torch.Tensor, value: torch.Tensor,
                sign1_indices: Optional[torch.Tensor] = None, 
                sign2_indices: Optional[torch.Tensor] = None,
                aspect_indices: Optional[torch.Tensor] = None) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Forward pass with astrological attention
        
        Args:
            query: Query tensor [batch_size, seq_len, embed_dim]
            key: Key tensor [batch_size, seq_len, embed_dim]  
            value: Value tensor [batch_size, seq_len, embed_dim]
            sign1_indices: First sign indices for bias [batch_size]
            sign2_indices: Second sign indices for bias [batch_size]
            aspect_indices: Aspect indices for bias [batch_size]
            
        Returns:
            Attended output and attention weights
        """
        batch_size, seq_len, embed_dim = query.size()
        
        # Project to Q, K, V
        Q = self.q_projection(query).view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        K = self.k_projection(key).view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        V = self.v_projection(value).view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        
        # Scaled dot-product attention
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.head_dim)
        
        # Apply learnable temperature
        scores = scores * self.temperature.view(1, -1, 1, 1)
        
        # Add astrological biases if provided
        if sign1_indices is not None and sign2_indices is not None:
            zodiac_bias = self._get_zodiac_bias(sign1_indices, sign2_indices, batch_size, seq_len)
            scores = scores + zodiac_bias
        
        if aspect_indices is not None:
            aspect_bias = self._get_aspect_bias(aspect_indices, batch_size, seq_len)
            scores = scores + aspect_bias
        
        # Apply softmax
        attention_weights = F.softmax(scores, dim=-1)
        attention_weights = self.dropout_layer(attention_weights)
        
        # Apply attention to values
        attended = torch.matmul(attention_weights, V)
        
        # Reshape and project output
        attended = attended.transpose(1, 2).contiguous().view(batch_size, seq_len, embed_dim)
        output = self.out_projection(attended)
        
        return output, attention_weights
    
    def _get_zodiac_bias(self, sign1_indices: torch.Tensor, sign2_indices: torch.Tensor, 
                        batch_size: int, seq_len: int) -> torch.Tensor:
        """Get zodiac compatibility bias for attention"""
        bias = torch.zeros(batch_size, self.num_heads, seq_len, seq_len)
        
        for batch_idx in range(batch_size):
            s1 = sign1_indices[batch_idx].item()
            s2 = sign2_indices[batch_idx].item()
            
            # Apply bias to sign-sign interactions
            if seq_len >= 2:  # Assuming first two positions are the signs
                bias[batch_idx, :, 0, 1] = self.zodiac_bias[s1, s2]
                bias[batch_idx, :, 1, 0] = self.zodiac_bias[s2, s1]
        
        if sign1_indices.is_cuda:
            bias = bias.cuda()
            
        return bias
    
    def _get_aspect_bias(self, aspect_indices: torch.Tensor, 
                        batch_size: int, seq_len: int) -> torch.Tensor:
        """Get aspect bias for attention"""
        bias = torch.zeros(batch_size, self.num_heads, seq_len, seq_len)
        
        for batch_idx in range(batch_size):
            aspect_idx = aspect_indices[batch_idx].item()
            if aspect_idx < 12:  # Valid aspect
                # Apply aspect bias to sign interactions
                if seq_len >= 2:
                    aspect_strength = self.aspect_bias[aspect_idx]
                    bias[batch_idx, :, 0, 1] += aspect_strength
                    bias[batch_idx, :, 1, 0] += aspect_strength
        
        if aspect_indices.is_cuda:
            bias = bias.cuda()
            
        return bias


class CrossSignAttention(nn.Module):
    """
    Cross-attention mechanism for analyzing interactions between different zodiac signs
    """
    
    def __init__(self, embed_dim: int, num_heads: int = 8):
        super().__init__()
        
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        
        self.attention = AstrologicalAttention(embed_dim, num_heads)
        
        # Position-wise feed forward
        self.feed_forward = nn.Sequential(
            nn.Linear(embed_dim, embed_dim * 4),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(embed_dim * 4, embed_dim)
        )
        
        # Layer normalization
        self.norm1 = nn.LayerNorm(embed_dim)
        self.norm2 = nn.LayerNorm(embed_dim)
        
        self.dropout = nn.Dropout(0.1)
    
    def forward(self, sign1_features: torch.Tensor, sign2_features: torch.Tensor,
                sign1_indices: Optional[torch.Tensor] = None,
                sign2_indices: Optional[torch.Tensor] = None) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Cross-attention between two sets of sign features
        
        Args:
            sign1_features: Features for first signs [batch_size, embed_dim]
            sign2_features: Features for second signs [batch_size, embed_dim]
            sign1_indices: Indices for first signs [batch_size]
            sign2_indices: Indices for second signs [batch_size]
            
        Returns:
            Cross-attended features and attention weights
        """
        batch_size = sign1_features.size(0)
        
        # Stack features for sequence processing
        combined_features = torch.stack([sign1_features, sign2_features], dim=1)  # [batch_size, 2, embed_dim]
        
        # Self-attention with astrological bias
        attended_features, attention_weights = self.attention(
            combined_features, combined_features, combined_features,
            sign1_indices, sign2_indices
        )
        
        # Residual connection and normalization
        attended_features = self.norm1(attended_features + combined_features)
        
        # Feed forward
        ff_output = self.feed_forward(attended_features)
        output = self.norm2(attended_features + self.dropout(ff_output))
        
        return output, attention_weights


class TemporalAttention(nn.Module):
    """
    Attention mechanism for temporal variations in compatibility
    Accounts for planetary transits, moon phases, etc.
    """
    
    def __init__(self, embed_dim: int, num_heads: int = 4):
        super().__init__()
        
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        
        # Temporal encoding
        self.temporal_encoding = nn.Sequential(
            nn.Linear(8, embed_dim),  # [hour, day, month, year, moon_phase, mercury_retrograde, etc.]
            nn.ReLU(),
            nn.Linear(embed_dim, embed_dim)
        )
        
        # Temporal attention
        self.attention = nn.MultiheadAttention(
            embed_dim=embed_dim,
            num_heads=num_heads,
            dropout=0.1,
            batch_first=True
        )
        
        # Temporal modulation weights
        self.temporal_weights = nn.Parameter(torch.ones(embed_dim))
        
    def forward(self, features: torch.Tensor, 
                temporal_context: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Apply temporal attention to compatibility features
        
        Args:
            features: Base compatibility features [batch_size, seq_len, embed_dim]
            temporal_context: Temporal context [batch_size, 8]
            
        Returns:
            Temporally adjusted features and attention weights
        """
        batch_size, seq_len = features.size(0), features.size(1)
        
        # Encode temporal context
        temporal_emb = self.temporal_encoding(temporal_context)  # [batch_size, embed_dim]
        temporal_emb = temporal_emb.unsqueeze(1)  # [batch_size, 1, embed_dim]
        
        # Expand temporal embedding to match sequence length
        temporal_sequence = temporal_emb.expand(-1, seq_len, -1)
        
        # Apply temporal attention
        attended_features, attention_weights = self.attention(
            features, temporal_sequence, temporal_sequence
        )
        
        # Apply temporal modulation
        modulated_features = attended_features * self.temporal_weights.unsqueeze(0).unsqueeze(0)
        
        return modulated_features, attention_weights


class HierarchicalAttention(nn.Module):
    """
    Hierarchical attention for multi-level compatibility analysis
    Sign-level -> Element-level -> Modality-level attention
    """
    
    def __init__(self, embed_dim: int):
        super().__init__()
        
        self.embed_dim = embed_dim
        
        # Different attention levels
        self.sign_attention = AstrologicalAttention(embed_dim, num_heads=8)
        self.element_attention = AstrologicalAttention(embed_dim // 2, num_heads=4)
        self.modality_attention = AstrologicalAttention(embed_dim // 4, num_heads=2)
        
        # Projection layers for different levels
        self.element_projection = nn.Linear(embed_dim, embed_dim // 2)
        self.modality_projection = nn.Linear(embed_dim // 2, embed_dim // 4)
        
        # Combination layer
        self.combination_layer = nn.Linear(
            embed_dim + embed_dim // 2 + embed_dim // 4, 
            embed_dim
        )
        
        # Element and modality mappings
        self.sign_to_element = torch.tensor([0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3])
        self.sign_to_modality = torch.tensor([0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2])
        
    def forward(self, features: torch.Tensor, 
                sign1_indices: torch.Tensor, 
                sign2_indices: torch.Tensor) -> torch.Tensor:
        """
        Apply hierarchical attention at multiple astrological levels
        
        Args:
            features: Input features [batch_size, seq_len, embed_dim]
            sign1_indices: First sign indices [batch_size]
            sign2_indices: Second sign indices [batch_size]
            
        Returns:
            Hierarchically attended features [batch_size, seq_len, embed_dim]
        """
        # Sign-level attention
        sign_attended, _ = self.sign_attention(
            features, features, features,
            sign1_indices, sign2_indices
        )
        
        # Element-level attention
        element_features = self.element_projection(sign_attended)
        element_indices1 = self.sign_to_element[sign1_indices]
        element_indices2 = self.sign_to_element[sign2_indices]
        
        if features.is_cuda:
            element_indices1 = element_indices1.cuda()
            element_indices2 = element_indices2.cuda()
            
        element_attended, _ = self.element_attention(
            element_features, element_features, element_features,
            element_indices1, element_indices2
        )
        
        # Modality-level attention
        modality_features = self.modality_projection(element_attended)
        modality_indices1 = self.sign_to_modality[sign1_indices]
        modality_indices2 = self.sign_to_modality[sign2_indices]
        
        if features.is_cuda:
            modality_indices1 = modality_indices1.cuda()
            modality_indices2 = modality_indices2.cuda()
            
        modality_attended, _ = self.modality_attention(
            modality_features, modality_features, modality_features,
            modality_indices1, modality_indices2
        )
        
        # Combine all levels
        combined_features = torch.cat([
            sign_attended,
            element_attended,
            modality_attended
        ], dim=-1)
        
        output = self.combination_layer(combined_features)
        
        return output


class AttentionVisualizer:
    """
    Utility class for visualizing and interpreting attention patterns
    """
    
    @staticmethod
    def extract_attention_patterns(attention_weights: torch.Tensor, 
                                 sign1_indices: torch.Tensor,
                                 sign2_indices: torch.Tensor) -> dict:
        """
        Extract interpretable attention patterns
        
        Args:
            attention_weights: Attention weights [batch_size, num_heads, seq_len, seq_len]
            sign1_indices: First sign indices [batch_size]
            sign2_indices: Second sign indices [batch_size]
            
        Returns:
            Dictionary of attention patterns and interpretations
        """
        batch_size, num_heads, seq_len, _ = attention_weights.size()
        
        patterns = {
            'sign_to_sign_attention': [],
            'head_specialization': [],
            'compatibility_strength': []
        }
        
        sign_names = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                     'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
        
        with torch.no_grad():
            for batch_idx in range(batch_size):
                s1 = sign1_indices[batch_idx].item()
                s2 = sign2_indices[batch_idx].item()
                
                # Extract sign-to-sign attention (assuming positions 0 and 1)
                if seq_len >= 2:
                    sign_attention = attention_weights[batch_idx, :, 0, 1].cpu().numpy()
                    patterns['sign_to_sign_attention'].append({
                        'signs': f"{sign_names[s1]} -> {sign_names[s2]}",
                        'attention_by_head': sign_attention.tolist(),
                        'average_attention': float(np.mean(sign_attention))
                    })
                
                # Head specialization analysis
                head_specialization = []
                for head in range(num_heads):
                    head_weights = attention_weights[batch_idx, head].cpu().numpy()
                    entropy = -np.sum(head_weights * np.log(head_weights + 1e-8))
                    head_specialization.append({
                        'head': head,
                        'entropy': float(entropy),
                        'focus': 'focused' if entropy < 1.0 else 'distributed'
                    })
                
                patterns['head_specialization'].append(head_specialization)
                
                # Overall compatibility strength
                avg_attention = torch.mean(attention_weights[batch_idx]).item()
                patterns['compatibility_strength'].append({
                    'signs': f"{sign_names[s1]} & {sign_names[s2]}",
                    'strength': float(avg_attention),
                    'interpretation': AttentionVisualizer._interpret_strength(avg_attention)
                })
        
        return patterns
    
    @staticmethod
    def _interpret_strength(strength: float) -> str:
        """Interpret attention strength"""
        if strength > 0.7:
            return "Very Strong Connection"
        elif strength > 0.5:
            return "Strong Connection"
        elif strength > 0.3:
            return "Moderate Connection"
        else:
            return "Weak Connection"


if __name__ == "__main__":
    # Test attention mechanisms
    embed_dim = 512
    batch_size = 4
    seq_len = 2
    
    # Test AstrologicalAttention
    attention = AstrologicalAttention(embed_dim, num_heads=8)
    
    features = torch.randn(batch_size, seq_len, embed_dim)
    sign1_indices = torch.tensor([0, 3, 6, 9])  # Aries, Cancer, Libra, Capricorn
    sign2_indices = torch.tensor([4, 7, 10, 1]) # Leo, Scorpio, Aquarius, Taurus
    
    output, weights = attention(features, features, features, sign1_indices, sign2_indices)
    print(f"Astrological attention output shape: {output.shape}")
    print(f"Attention weights shape: {weights.shape}")
    
    # Test CrossSignAttention
    cross_attention = CrossSignAttention(embed_dim)
    sign1_features = torch.randn(batch_size, embed_dim)
    sign2_features = torch.randn(batch_size, embed_dim)
    
    cross_output, cross_weights = cross_attention(sign1_features, sign2_features, sign1_indices, sign2_indices)
    print(f"Cross attention output shape: {cross_output.shape}")
    
    # Test attention visualization
    visualizer = AttentionVisualizer()
    patterns = visualizer.extract_attention_patterns(weights, sign1_indices, sign2_indices)
    print(f"Extracted {len(patterns['sign_to_sign_attention'])} attention patterns")