import torch
import torch.nn as nn
import torch.nn.functional as F
import math
from typing import Optional, Dict, List, Tuple
from .attention import AstrologicalAttention, CrossSignAttention, HierarchicalAttention

class AstrologicalTransformerBlock(nn.Module):
    """
    Transformer block specifically designed for astrological compatibility analysis
    Incorporates zodiac-aware attention and astrological knowledge
    """
    
    def __init__(self, embed_dim: int, num_heads: int = 8, ff_dim: Optional[int] = None, 
                 dropout: float = 0.1):
        super().__init__()
        
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.ff_dim = ff_dim or 4 * embed_dim
        
        # Multi-head astrological attention
        self.attention = AstrologicalAttention(embed_dim, num_heads, dropout)
        
        # Feed-forward network
        self.feed_forward = nn.Sequential(
            nn.Linear(embed_dim, self.ff_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(self.ff_dim, embed_dim),
            nn.Dropout(dropout)
        )
        
        # Layer normalization
        self.norm1 = nn.LayerNorm(embed_dim)
        self.norm2 = nn.LayerNorm(embed_dim)
        
        # Astrological gate for controlling information flow
        self.astrological_gate = nn.Sequential(
            nn.Linear(embed_dim, embed_dim),
            nn.Sigmoid()
        )
        
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x: torch.Tensor, 
                sign1_indices: Optional[torch.Tensor] = None,
                sign2_indices: Optional[torch.Tensor] = None,
                aspect_indices: Optional[torch.Tensor] = None) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Forward pass through the transformer block
        
        Args:
            x: Input features [batch_size, seq_len, embed_dim]
            sign1_indices: First sign indices [batch_size]
            sign2_indices: Second sign indices [batch_size]
            aspect_indices: Aspect indices [batch_size]
            
        Returns:
            Output features and attention weights
        """
        # Self-attention with astrological bias
        attended, attention_weights = self.attention(
            x, x, x, sign1_indices, sign2_indices, aspect_indices
        )
        
        # First residual connection
        x_attended = self.norm1(x + self.dropout(attended))
        
        # Apply astrological gate
        gate = self.astrological_gate(x_attended)
        x_gated = x_attended * gate
        
        # Feed-forward network
        ff_output = self.feed_forward(x_gated)
        
        # Second residual connection
        output = self.norm2(x_attended + ff_output)
        
        return output, attention_weights


class CompatibilityTransformer(nn.Module):
    """
    Complete transformer architecture for zodiac compatibility analysis
    Multi-layer transformer with specialized astrological processing
    """
    
    def __init__(self, embed_dim: int = 512, num_layers: int = 6, num_heads: int = 8, 
                 ff_dim: Optional[int] = None, dropout: float = 0.1):
        super().__init__()
        
        self.embed_dim = embed_dim
        self.num_layers = num_layers
        self.num_heads = num_heads
        
        # Stack of transformer blocks
        self.layers = nn.ModuleList([
            AstrologicalTransformerBlock(embed_dim, num_heads, ff_dim, dropout)
            for _ in range(num_layers)
        ])
        
        # Hierarchical attention for multi-level analysis
        self.hierarchical_attention = HierarchicalAttention(embed_dim)
        
        # Cross-sign interaction layer
        self.cross_sign_attention = CrossSignAttention(embed_dim, num_heads)
        
        # Output normalization
        self.final_norm = nn.LayerNorm(embed_dim)
        
        # Compatibility dimension heads
        self.compatibility_heads = nn.ModuleDict({
            'love': nn.Linear(embed_dim, 1),
            'friendship': nn.Linear(embed_dim, 1),
            'communication': nn.Linear(embed_dim, 1),
            'emotional': nn.Linear(embed_dim, 1),
            'intellectual': nn.Linear(embed_dim, 1),
            'physical': nn.Linear(embed_dim, 1),
            'spiritual': nn.Linear(embed_dim, 1),
            'career': nn.Linear(embed_dim, 1),
            'family': nn.Linear(embed_dim, 1),
            'trust': nn.Linear(embed_dim, 1),
            'values': nn.Linear(embed_dim, 1),
            'overall': nn.Linear(embed_dim, 1)
        })
        
    def forward(self, x: torch.Tensor,
                sign1_indices: torch.Tensor,
                sign2_indices: torch.Tensor,
                aspect_indices: Optional[torch.Tensor] = None) -> Dict[str, torch.Tensor]:
        """
        Forward pass through the compatibility transformer
        
        Args:
            x: Input features [batch_size, seq_len, embed_dim]
            sign1_indices: First sign indices [batch_size]
            sign2_indices: Second sign indices [batch_size] 
            aspect_indices: Aspect indices [batch_size]
            
        Returns:
            Dictionary of compatibility scores for each dimension
        """
        batch_size = x.size(0)
        all_attention_weights = []
        
        # Pass through transformer layers
        for layer in self.layers:
            x, attention_weights = layer(x, sign1_indices, sign2_indices, aspect_indices)
            all_attention_weights.append(attention_weights)
        
        # Apply hierarchical attention
        x = self.hierarchical_attention(x, sign1_indices, sign2_indices)
        
        # Cross-sign attention if we have multiple signs
        if x.size(1) >= 2:
            sign1_features = x[:, 0, :]  # [batch_size, embed_dim]
            sign2_features = x[:, 1, :]  # [batch_size, embed_dim]
            
            cross_attended, cross_weights = self.cross_sign_attention(
                sign1_features, sign2_features, sign1_indices, sign2_indices
            )
            
            # Use the combined features from cross-attention
            final_features = torch.mean(cross_attended, dim=1)  # [batch_size, embed_dim]
        else:
            final_features = torch.mean(x, dim=1)  # Global average pooling
        
        # Final normalization
        final_features = self.final_norm(final_features)
        
        # Generate compatibility scores for each dimension
        compatibility_scores = {}
        for dimension, head in self.compatibility_heads.items():
            score = torch.sigmoid(head(final_features))  # [batch_size, 1]
            compatibility_scores[dimension] = score.squeeze(-1)  # [batch_size]
        
        # Store attention weights for interpretability
        compatibility_scores['attention_weights'] = all_attention_weights
        
        return compatibility_scores
    
    def get_attention_patterns(self, x: torch.Tensor,
                             sign1_indices: torch.Tensor,
                             sign2_indices: torch.Tensor) -> Dict[str, torch.Tensor]:
        """
        Extract attention patterns for interpretability
        
        Returns:
            Dictionary of attention patterns from different layers
        """
        patterns = {}
        
        with torch.no_grad():
            current_x = x
            
            for layer_idx, layer in enumerate(self.layers):
                _, attention_weights = layer(current_x, sign1_indices, sign2_indices)
                patterns[f'layer_{layer_idx}'] = attention_weights
                
                # Update current_x for next layer
                current_x, _ = layer(current_x, sign1_indices, sign2_indices)
        
        return patterns


class TransformerEncoder(nn.Module):
    """
    Standard transformer encoder with positional encoding for sequence processing
    """
    
    def __init__(self, embed_dim: int = 512, num_layers: int = 6, num_heads: int = 8,
                 ff_dim: int = 2048, max_seq_len: int = 100, dropout: float = 0.1):
        super().__init__()
        
        self.embed_dim = embed_dim
        self.max_seq_len = max_seq_len
        
        # Positional encoding
        self.pos_encoding = self._create_positional_encoding(embed_dim, max_seq_len)
        
        # Transformer encoder layers
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embed_dim,
            nhead=num_heads,
            dim_feedforward=ff_dim,
            dropout=dropout,
            activation='gelu',
            batch_first=True
        )
        
        self.transformer_encoder = nn.TransformerEncoder(
            encoder_layer,
            num_layers=num_layers
        )
        
        self.dropout = nn.Dropout(dropout)
        
    def _create_positional_encoding(self, embed_dim: int, max_len: int) -> torch.Tensor:
        """Create sinusoidal positional encodings"""
        pe = torch.zeros(max_len, embed_dim)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        
        div_term = torch.exp(torch.arange(0, embed_dim, 2).float() * 
                           (-math.log(10000.0) / embed_dim))
        
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        
        return pe.unsqueeze(0)  # [1, max_len, embed_dim]
    
    def forward(self, x: torch.Tensor, mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        Forward pass with positional encoding
        
        Args:
            x: Input sequences [batch_size, seq_len, embed_dim]
            mask: Optional attention mask [seq_len, seq_len]
            
        Returns:
            Encoded sequences [batch_size, seq_len, embed_dim]
        """
        batch_size, seq_len = x.size(0), x.size(1)
        
        # Add positional encoding
        if seq_len <= self.max_seq_len:
            pos_enc = self.pos_encoding[:, :seq_len, :]
            if x.is_cuda:
                pos_enc = pos_enc.cuda()
            x = x + pos_enc
        
        x = self.dropout(x)
        
        # Apply transformer encoder
        output = self.transformer_encoder(x, mask=mask)
        
        return output


class CompatibilityDecoder(nn.Module):
    """
    Decoder for generating detailed compatibility analysis
    """
    
    def __init__(self, embed_dim: int = 512, num_layers: int = 3, num_heads: int = 8):
        super().__init__()
        
        self.embed_dim = embed_dim
        
        # Decoder layers
        decoder_layer = nn.TransformerDecoderLayer(
            d_model=embed_dim,
            nhead=num_heads,
            dim_feedforward=embed_dim * 4,
            dropout=0.1,
            activation='gelu',
            batch_first=True
        )
        
        self.transformer_decoder = nn.TransformerDecoder(
            decoder_layer,
            num_layers=num_layers
        )
        
        # Analysis generation heads
        self.analysis_heads = nn.ModuleDict({
            'strengths': nn.Linear(embed_dim, 256),
            'challenges': nn.Linear(embed_dim, 256),
            'advice': nn.Linear(embed_dim, 256),
            'summary': nn.Linear(embed_dim, 256)
        })
        
    def forward(self, encoder_output: torch.Tensor, 
                target_queries: torch.Tensor) -> Dict[str, torch.Tensor]:
        """
        Generate detailed compatibility analysis
        
        Args:
            encoder_output: Encoded compatibility features [batch_size, seq_len, embed_dim]
            target_queries: Query vectors for different analysis types [batch_size, num_queries, embed_dim]
            
        Returns:
            Dictionary of analysis components
        """
        # Apply transformer decoder
        decoded_features = self.transformer_decoder(target_queries, encoder_output)
        
        # Generate different analysis components
        analysis = {}
        for component, head in self.analysis_heads.items():
            # Use specific query for each component
            query_idx = list(self.analysis_heads.keys()).index(component)
            if query_idx < decoded_features.size(1):
                component_features = decoded_features[:, query_idx, :]
                analysis[component] = head(component_features)
        
        return analysis


class CompatibilityTransformerLarge(nn.Module):
    """
    Large-scale transformer for high-accuracy compatibility analysis
    """
    
    def __init__(self, embed_dim: int = 768, num_layers: int = 12, num_heads: int = 12):
        super().__init__()
        
        # Encoder
        self.encoder = TransformerEncoder(
            embed_dim=embed_dim,
            num_layers=num_layers,
            num_heads=num_heads,
            ff_dim=embed_dim * 4
        )
        
        # Specialized compatibility transformer
        self.compatibility_transformer = CompatibilityTransformer(
            embed_dim=embed_dim,
            num_layers=6,
            num_heads=num_heads
        )
        
        # Decoder for detailed analysis
        self.decoder = CompatibilityDecoder(
            embed_dim=embed_dim,
            num_layers=4,
            num_heads=num_heads
        )
        
        # Analysis query embeddings
        self.analysis_queries = nn.Parameter(torch.randn(4, embed_dim))  # strengths, challenges, advice, summary
        
    def forward(self, input_features: torch.Tensor,
                sign1_indices: torch.Tensor,
                sign2_indices: torch.Tensor) -> Dict[str, torch.Tensor]:
        """
        Complete forward pass for large-scale compatibility analysis
        
        Args:
            input_features: Input features [batch_size, seq_len, embed_dim]
            sign1_indices: First sign indices [batch_size]
            sign2_indices: Second sign indices [batch_size]
            
        Returns:
            Comprehensive compatibility analysis
        """
        batch_size = input_features.size(0)
        
        # Encode input features
        encoded_features = self.encoder(input_features)
        
        # Get compatibility scores
        compatibility_scores = self.compatibility_transformer(
            encoded_features, sign1_indices, sign2_indices
        )
        
        # Generate detailed analysis
        analysis_queries = self.analysis_queries.unsqueeze(0).expand(batch_size, -1, -1)
        detailed_analysis = self.decoder(encoded_features, analysis_queries)
        
        # Combine results
        results = {
            'compatibility_scores': compatibility_scores,
            'detailed_analysis': detailed_analysis,
            'encoded_features': encoded_features
        }
        
        return results


if __name__ == "__main__":
    # Test transformer components
    embed_dim = 512
    batch_size = 4
    seq_len = 2
    
    # Test AstrologicalTransformerBlock
    transformer_block = AstrologicalTransformerBlock(embed_dim)
    
    x = torch.randn(batch_size, seq_len, embed_dim)
    sign1_indices = torch.tensor([0, 3, 6, 9])
    sign2_indices = torch.tensor([4, 7, 10, 1])
    
    output, attention = transformer_block(x, sign1_indices, sign2_indices)
    print(f"Transformer block output shape: {output.shape}")
    print(f"Attention weights shape: {attention.shape}")
    
    # Test CompatibilityTransformer
    compatibility_transformer = CompatibilityTransformer(embed_dim, num_layers=3)
    
    compatibility_scores = compatibility_transformer(x, sign1_indices, sign2_indices)
    print(f"Compatibility dimensions: {list(compatibility_scores.keys())}")
    print(f"Love compatibility shape: {compatibility_scores['love'].shape}")
    
    # Test TransformerEncoder
    encoder = TransformerEncoder(embed_dim, num_layers=3)
    encoded = encoder(x)
    print(f"Encoded features shape: {encoded.shape}")
    
    # Test large transformer
    large_transformer = CompatibilityTransformerLarge(embed_dim=512, num_layers=6, num_heads=8)
    results = large_transformer(x, sign1_indices, sign2_indices)
    print(f"Large transformer results keys: {list(results.keys())}")
    print(f"Compatibility scores keys: {list(results['compatibility_scores'].keys())}")
    print(f"Detailed analysis keys: {list(results['detailed_analysis'].keys())}")