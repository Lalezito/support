import torch
import torch.nn as nn
import numpy as np
from typing import Dict, List, Optional
import math

class ZodiacEmbeddings(nn.Module):
    """
    Advanced embedding system for zodiac signs with astrological knowledge integration
    """
    
    def __init__(self, embedding_dim: int = 512):
        super().__init__()
        
        self.embedding_dim = embedding_dim
        
        # Core zodiac sign embeddings
        self.sign_embeddings = nn.Embedding(12, embedding_dim)
        
        # Astrological attribute embeddings
        self.element_embeddings = nn.Embedding(4, embedding_dim // 4)  # Fire, Earth, Air, Water
        self.modality_embeddings = nn.Embedding(3, embedding_dim // 4)  # Cardinal, Fixed, Mutable
        self.polarity_embeddings = nn.Embedding(2, embedding_dim // 8)  # Positive/Negative
        
        # Planet ruler embeddings
        self.planet_embeddings = nn.Embedding(10, embedding_dim // 4)  # Traditional planets
        
        # House position embeddings (1-12 houses)
        self.house_embeddings = nn.Embedding(12, embedding_dim // 8)
        
        # Aspect embeddings (conjunction, opposition, trine, square, sextile, etc.)
        self.aspect_embeddings = nn.Embedding(12, embedding_dim // 2)
        
        # Temporal embeddings for time-based variations
        self.temporal_embeddings = self._create_temporal_embeddings()
        
        # Combine different embedding components
        self.projection = nn.Linear(
            embedding_dim + embedding_dim//4 + embedding_dim//4 + embedding_dim//8 + embedding_dim//4,
            embedding_dim
        )
        
        self._initialize_astrological_knowledge()
        
    def _create_temporal_embeddings(self) -> nn.Module:
        """Create sinusoidal temporal embeddings for time variations"""
        return nn.Sequential(
            nn.Linear(4, self.embedding_dim // 8),  # [hour, day, month, year]
            nn.ReLU(),
            nn.Linear(self.embedding_dim // 8, self.embedding_dim // 8)
        )
        
    def _initialize_astrological_knowledge(self):
        """Initialize embeddings with astrological knowledge"""
        
        # Zodiac sign to element mapping
        self.sign_to_element = {
            0: 0,  # Aries -> Fire
            1: 1,  # Taurus -> Earth  
            2: 2,  # Gemini -> Air
            3: 3,  # Cancer -> Water
            4: 0,  # Leo -> Fire
            5: 1,  # Virgo -> Earth
            6: 2,  # Libra -> Air
            7: 3,  # Scorpio -> Water
            8: 0,  # Sagittarius -> Fire
            9: 1,  # Capricorn -> Earth
            10: 2, # Aquarius -> Air
            11: 3  # Pisces -> Water
        }
        
        # Zodiac sign to modality mapping
        self.sign_to_modality = {
            0: 0, 3: 0, 6: 0, 9: 0,    # Cardinal: Aries, Cancer, Libra, Capricorn
            1: 1, 4: 1, 7: 1, 10: 1,   # Fixed: Taurus, Leo, Scorpio, Aquarius
            2: 2, 5: 2, 8: 2, 11: 2    # Mutable: Gemini, Virgo, Sagittarius, Pisces
        }
        
        # Zodiac sign to polarity mapping
        self.sign_to_polarity = {
            0: 1, 2: 1, 4: 1, 6: 1, 8: 1, 10: 1,  # Positive: Fire & Air
            1: 0, 3: 0, 5: 0, 7: 0, 9: 0, 11: 0   # Negative: Earth & Water
        }
        
        # Planet rulers for each sign
        self.sign_to_planet = {
            0: 0,  # Aries -> Mars
            1: 1,  # Taurus -> Venus
            2: 2,  # Gemini -> Mercury
            3: 3,  # Cancer -> Moon
            4: 4,  # Leo -> Sun
            5: 2,  # Virgo -> Mercury
            6: 1,  # Libra -> Venus
            7: 5,  # Scorpio -> Pluto (traditional Mars)
            8: 6,  # Sagittarius -> Jupiter
            9: 7,  # Capricorn -> Saturn
            10: 8, # Aquarius -> Uranus (traditional Saturn)
            11: 9  # Pisces -> Neptune (traditional Jupiter)
        }
        
    def get_sign_attributes(self, sign_idx: torch.Tensor) -> Dict[str, torch.Tensor]:
        """Get all astrological attributes for given signs"""
        batch_size = sign_idx.size(0)
        
        # Map signs to their attributes
        element_indices = torch.tensor([self.sign_to_element[idx.item()] for idx in sign_idx])
        modality_indices = torch.tensor([self.sign_to_modality[idx.item()] for idx in sign_idx])
        polarity_indices = torch.tensor([self.sign_to_polarity[idx.item()] for idx in sign_idx])
        planet_indices = torch.tensor([self.sign_to_planet[idx.item()] for idx in sign_idx])
        
        if sign_idx.is_cuda:
            element_indices = element_indices.cuda()
            modality_indices = modality_indices.cuda()
            polarity_indices = polarity_indices.cuda()
            planet_indices = planet_indices.cuda()
            
        return {
            'element': element_indices,
            'modality': modality_indices,
            'polarity': polarity_indices,
            'planet': planet_indices
        }
    
    def forward(self, sign_indices: torch.Tensor, 
                temporal_context: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        Create enriched embeddings combining multiple astrological factors
        
        Args:
            sign_indices: Zodiac sign indices [batch_size]
            temporal_context: Optional temporal context [batch_size, 4] (hour, day, month, year)
            
        Returns:
            Enhanced embeddings [batch_size, embedding_dim]
        """
        batch_size = sign_indices.size(0)
        
        # Get basic sign embeddings
        sign_emb = self.sign_embeddings(sign_indices)
        
        # Get astrological attributes
        attributes = self.get_sign_attributes(sign_indices)
        
        # Get attribute embeddings
        element_emb = self.element_embeddings(attributes['element'])
        modality_emb = self.modality_embeddings(attributes['modality'])
        polarity_emb = self.polarity_embeddings(attributes['polarity'])
        planet_emb = self.planet_embeddings(attributes['planet'])
        
        # Combine core embeddings
        combined_emb = torch.cat([
            sign_emb,
            element_emb,
            modality_emb, 
            polarity_emb,
            planet_emb
        ], dim=-1)
        
        # Project to final embedding dimension
        final_embedding = self.projection(combined_emb)
        
        # Add temporal context if provided
        if temporal_context is not None:
            temporal_emb = self.temporal_embeddings(temporal_context)
            final_embedding = final_embedding + temporal_emb
            
        return final_embedding


class AspectEmbeddings(nn.Module):
    """
    Specialized embeddings for astrological aspects between signs
    """
    
    def __init__(self, embedding_dim: int = 256):
        super().__init__()
        
        self.embedding_dim = embedding_dim
        
        # Major aspects embeddings
        self.aspect_embeddings = nn.Embedding(12, embedding_dim)
        
        # Aspect strength embeddings (tight, moderate, wide orbs)
        self.strength_embeddings = nn.Embedding(3, embedding_dim // 4)
        
        # Aspect type embeddings (harmonious, challenging, neutral)
        self.type_embeddings = nn.Embedding(3, embedding_dim // 4)
        
        # Define aspect characteristics
        self._initialize_aspect_knowledge()
        
    def _initialize_aspect_knowledge(self):
        """Initialize aspect knowledge"""
        
        # Aspect angles and their meanings
        self.aspect_info = {
            0: {'angle': 0, 'name': 'Conjunction', 'type': 2, 'strength': 2},      # Neutral, Very Strong
            1: {'angle': 30, 'name': 'Semi-sextile', 'type': 2, 'strength': 0},    # Neutral, Weak
            2: {'angle': 45, 'name': 'Semi-square', 'type': 1, 'strength': 1},     # Challenging, Moderate
            3: {'angle': 60, 'name': 'Sextile', 'type': 0, 'strength': 1},        # Harmonious, Moderate
            4: {'angle': 90, 'name': 'Square', 'type': 1, 'strength': 2},         # Challenging, Strong
            5: {'angle': 120, 'name': 'Trine', 'type': 0, 'strength': 2},         # Harmonious, Strong
            6: {'angle': 135, 'name': 'Sesquiquadrate', 'type': 1, 'strength': 1}, # Challenging, Moderate
            7: {'angle': 150, 'name': 'Quincunx', 'type': 2, 'strength': 1},      # Neutral, Moderate
            8: {'angle': 180, 'name': 'Opposition', 'type': 1, 'strength': 2},    # Challenging, Strong
        }
    
    def calculate_aspect(self, sign1_idx: torch.Tensor, sign2_idx: torch.Tensor) -> torch.Tensor:
        """
        Calculate the primary aspect between two zodiac signs
        
        Args:
            sign1_idx: First sign indices [batch_size]
            sign2_idx: Second sign indices [batch_size]
            
        Returns:
            Aspect indices [batch_size]
        """
        # Calculate angle difference (each sign is 30 degrees apart)
        angle_diff = torch.abs(sign1_idx - sign2_idx) * 30
        
        # Handle wrap-around (e.g., Pisces to Aries)
        angle_diff = torch.min(angle_diff, 360 - angle_diff)
        
        # Map angles to aspect types (simplified)
        aspect_indices = torch.zeros_like(angle_diff)
        
        for batch_idx in range(angle_diff.size(0)):
            angle = angle_diff[batch_idx].item()
            
            if angle <= 5:  # Conjunction (0° ±5°)
                aspect_indices[batch_idx] = 0
            elif 55 <= angle <= 65:  # Sextile (60° ±5°)
                aspect_indices[batch_idx] = 3
            elif 85 <= angle <= 95:  # Square (90° ±5°)
                aspect_indices[batch_idx] = 4
            elif 115 <= angle <= 125:  # Trine (120° ±5°)
                aspect_indices[batch_idx] = 5
            elif 175 <= angle <= 185:  # Opposition (180° ±5°)
                aspect_indices[batch_idx] = 8
            else:
                aspect_indices[batch_idx] = 1  # Minor aspect
                
        return aspect_indices
    
    def forward(self, sign1_idx: torch.Tensor, sign2_idx: torch.Tensor) -> torch.Tensor:
        """
        Create aspect embeddings between two signs
        
        Args:
            sign1_idx: First sign indices [batch_size]
            sign2_idx: Second sign indices [batch_size]
            
        Returns:
            Aspect embeddings [batch_size, embedding_dim]
        """
        # Calculate primary aspect
        aspect_indices = self.calculate_aspect(sign1_idx, sign2_idx)
        
        # Get aspect embeddings
        aspect_emb = self.aspect_embeddings(aspect_indices)
        
        # Get strength and type embeddings based on aspect
        strength_indices = torch.tensor([
            self.aspect_info.get(idx.item(), {'strength': 0})['strength'] 
            for idx in aspect_indices
        ])
        type_indices = torch.tensor([
            self.aspect_info.get(idx.item(), {'type': 2})['type'] 
            for idx in aspect_indices
        ])
        
        if sign1_idx.is_cuda:
            strength_indices = strength_indices.cuda()
            type_indices = type_indices.cuda()
        
        strength_emb = self.strength_embeddings(strength_indices)
        type_emb = self.type_embeddings(type_indices)
        
        # Combine embeddings
        combined_emb = torch.cat([aspect_emb, strength_emb, type_emb], dim=-1)
        
        # Project back to embedding dimension
        if combined_emb.size(-1) != self.embedding_dim:
            projection = nn.Linear(combined_emb.size(-1), self.embedding_dim)
            if aspect_emb.is_cuda:
                projection = projection.cuda()
            combined_emb = projection(combined_emb)
            
        return combined_emb


class CompatibilityMatrix(nn.Module):
    """
    Generate learned compatibility matrices between zodiac signs
    """
    
    def __init__(self, num_signs: int = 12, matrix_dim: int = 64):
        super().__init__()
        
        self.num_signs = num_signs
        self.matrix_dim = matrix_dim
        
        # Learnable compatibility matrices for each dimension
        self.compatibility_matrices = nn.Parameter(
            torch.randn(12, num_signs, num_signs, matrix_dim)  # 12 compatibility dimensions
        )
        
        # Sign interaction weights
        self.interaction_weights = nn.Parameter(torch.randn(num_signs, num_signs))
        
        # Initialize with traditional compatibility knowledge
        self._initialize_traditional_compatibility()
        
    def _initialize_traditional_compatibility(self):
        """Initialize matrices with traditional astrological compatibility"""
        with torch.no_grad():
            # Initialize based on element compatibility
            element_compatibility = torch.tensor([
                [1.0, 0.3, 0.8, 0.3],  # Fire with Fire, Earth, Air, Water
                [0.3, 1.0, 0.3, 0.8],  # Earth with Fire, Earth, Air, Water  
                [0.8, 0.3, 1.0, 0.3],  # Air with Fire, Earth, Air, Water
                [0.3, 0.8, 0.3, 1.0]   # Water with Fire, Earth, Air, Water
            ])
            
            sign_to_element = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]  # Aries=Fire, etc.
            
            for i in range(self.num_signs):
                for j in range(self.num_signs):
                    element_i = sign_to_element[i]
                    element_j = sign_to_element[j]
                    compatibility_score = element_compatibility[element_i][element_j]
                    
                    # Initialize interaction weights
                    self.interaction_weights[i, j] = compatibility_score
                    
                    # Initialize compatibility matrices with element-based values
                    for dim in range(12):
                        self.compatibility_matrices[dim, i, j] = torch.randn(self.matrix_dim) * compatibility_score
    
    def forward(self, sign1_idx: torch.Tensor, sign2_idx: torch.Tensor) -> torch.Tensor:
        """
        Generate compatibility matrices for given sign pairs
        
        Args:
            sign1_idx: First sign indices [batch_size]
            sign2_idx: Second sign indices [batch_size]
            
        Returns:
            Compatibility matrices [batch_size, 12, matrix_dim]
        """
        batch_size = sign1_idx.size(0)
        
        compatibility_results = []
        
        for batch_idx in range(batch_size):
            s1 = sign1_idx[batch_idx].item()
            s2 = sign2_idx[batch_idx].item()
            
            # Get compatibility matrix for this pair across all dimensions
            pair_matrices = self.compatibility_matrices[:, s1, s2]  # [12, matrix_dim]
            compatibility_results.append(pair_matrices)
        
        return torch.stack(compatibility_results, dim=0)  # [batch_size, 12, matrix_dim]


if __name__ == "__main__":
    # Test embeddings
    zodiac_emb = ZodiacEmbeddings(embedding_dim=512)
    aspect_emb = AspectEmbeddings(embedding_dim=256)
    compat_matrix = CompatibilityMatrix()
    
    # Test data
    sign1 = torch.tensor([0, 3, 6])  # Aries, Cancer, Libra
    sign2 = torch.tensor([4, 7, 10]) # Leo, Scorpio, Aquarius
    
    # Test zodiac embeddings
    zodiac_features = zodiac_emb(sign1)
    print(f"Zodiac embeddings shape: {zodiac_features.shape}")
    
    # Test aspect embeddings  
    aspect_features = aspect_emb(sign1, sign2)
    print(f"Aspect embeddings shape: {aspect_features.shape}")
    
    # Test compatibility matrices
    compat_matrices = compat_matrix(sign1, sign2)
    print(f"Compatibility matrices shape: {compat_matrices.shape}")