import torch
import numpy as np
import random
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass
import copy

@dataclass
class CompatibilityAugmentationConfig:
    """Configuration for compatibility data augmentation"""
    temporal_shift_prob: float = 0.3
    context_noise_prob: float = 0.4
    sign_rotation_prob: float = 0.2
    aspect_perturbation_prob: float = 0.3
    compatibility_scaling_prob: float = 0.2
    seasonal_variation_prob: float = 0.25
    moon_phase_prob: float = 0.3
    retrograde_prob: float = 0.15
    
    # Augmentation strength parameters
    temporal_shift_range: Tuple[float, float] = (-0.1, 0.1)
    context_noise_std: float = 0.05
    aspect_perturbation_std: float = 0.02
    compatibility_scaling_range: Tuple[float, float] = (0.9, 1.1)
    
    # Preserve astrological integrity
    preserve_core_relationships: bool = True
    maintain_sign_order: bool = True

class CompatibilityDataAugmentation:
    """
    Advanced data augmentation for zodiac compatibility datasets
    Preserves astrological relationships while increasing data diversity
    """
    
    def __init__(self, config: CompatibilityAugmentationConfig = None):
        self.config = config or CompatibilityAugmentationConfig()
        
        # Astrological knowledge for preserving relationships
        self.element_groups = {
            'fire': [0, 4, 8],      # Aries, Leo, Sagittarius
            'earth': [1, 5, 9],     # Taurus, Virgo, Capricorn
            'air': [2, 6, 10],      # Gemini, Libra, Aquarius
            'water': [3, 7, 11]     # Cancer, Scorpio, Pisces
        }
        
        self.modality_groups = {
            'cardinal': [0, 3, 6, 9],    # Aries, Cancer, Libra, Capricorn
            'fixed': [1, 4, 7, 10],      # Taurus, Leo, Scorpio, Aquarius
            'mutable': [2, 5, 8, 11]     # Gemini, Virgo, Sagittarius, Pisces
        }
        
        # Traditional compatibility relationships
        self.compatibility_weights = self._initialize_compatibility_weights()
        
        # Augmentation strategies
        self.augmentation_strategies = [
            self.temporal_shift_augmentation,
            self.context_perturbation,
            self.sign_rotation_augmentation,
            self.aspect_perturbation,
            self.compatibility_scaling,
            self.seasonal_variation,
            self.moon_phase_variation,
            self.planetary_retrograde_effect
        ]
    
    def _initialize_compatibility_weights(self) -> np.ndarray:
        """Initialize compatibility weights based on traditional astrology"""
        weights = np.ones((12, 12))
        
        # Element compatibility (stronger relationships)
        for element, signs in self.element_groups.items():
            for s1 in signs:
                for s2 in signs:
                    if s1 != s2:
                        weights[s1, s2] = 1.2  # Same element compatibility
        
        # Complementary elements
        complementary_pairs = [
            ('fire', 'air'),    # Fire feeds on Air
            ('earth', 'water')  # Earth nourishes Water
        ]
        
        for elem1, elem2 in complementary_pairs:
            for s1 in self.element_groups[elem1]:
                for s2 in self.element_groups[elem2]:
                    weights[s1, s2] = 1.1
                    weights[s2, s1] = 1.1
        
        return weights
    
    def augment_dataset(self, dataset: List[Dict[str, Any]], 
                       augmentation_factor: int = 3) -> List[Dict[str, Any]]:
        """
        Apply data augmentation to increase dataset size
        
        Args:
            dataset: Original dataset
            augmentation_factor: Number of augmented versions per sample
            
        Returns:
            Augmented dataset
        """
        augmented_data = []
        
        # Include original data
        augmented_data.extend(dataset)
        
        # Generate augmented samples
        for original_sample in dataset:
            for _ in range(augmentation_factor):
                augmented_sample = self._augment_single_sample(original_sample)
                augmented_data.append(augmented_sample)
        
        return augmented_data
    
    def _augment_single_sample(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        """Apply random augmentation to a single sample"""
        augmented_sample = copy.deepcopy(sample)
        
        # Randomly select augmentation strategies
        num_augmentations = random.randint(1, 3)  # Apply 1-3 augmentations
        selected_strategies = random.sample(self.augmentation_strategies, num_augmentations)
        
        # Apply selected augmentations
        for strategy in selected_strategies:
            try:
                augmented_sample = strategy(augmented_sample)
            except Exception as e:
                # Skip failed augmentation
                continue
        
        return augmented_sample
    
    def temporal_shift_augmentation(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply temporal shifts to simulate time-based compatibility variations
        """
        if random.random() > self.config.temporal_shift_prob:
            return sample
        
        augmented_sample = copy.deepcopy(sample)
        
        # Add temporal context if it exists
        if 'temporal_context' in augmented_sample:
            temporal_context = augmented_sample['temporal_context']
            
            # Apply temporal shift
            shift_amount = random.uniform(*self.config.temporal_shift_range)
            
            # Shift different temporal components
            if isinstance(temporal_context, (list, np.ndarray)):
                temporal_context = np.array(temporal_context)
                # Shift time-related features (assuming first few are time-based)
                for i in range(min(4, len(temporal_context))):  # hour, day, month, year
                    temporal_context[i] += shift_amount
                    # Keep within valid ranges
                    if i == 0:  # hour
                        temporal_context[i] = temporal_context[i] % 24
                    elif i == 1:  # day
                        temporal_context[i] = np.clip(temporal_context[i], 1, 31)
                    elif i == 2:  # month
                        temporal_context[i] = np.clip(temporal_context[i], 1, 12)
                
                augmented_sample['temporal_context'] = temporal_context
        
        # Slight adjustment to compatibility scores based on temporal shift
        if 'targets' in augmented_sample:
            targets = np.array(augmented_sample['targets'])
            temporal_modifier = 1.0 + random.uniform(-0.02, 0.02)  # ±2% variation
            targets = np.clip(targets * temporal_modifier, 0, 1)
            augmented_sample['targets'] = targets
        
        return augmented_sample
    
    def context_perturbation(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        """Add noise to context features"""
        if random.random() > self.config.context_noise_prob:
            return sample
        
        augmented_sample = copy.deepcopy(sample)
        
        if 'context_features' in augmented_sample:
            context = np.array(augmented_sample['context_features'])
            
            # Add Gaussian noise
            noise = np.random.normal(0, self.config.context_noise_std, context.shape)
            noisy_context = context + noise
            
            # Ensure values remain in valid range [0, 1]
            noisy_context = np.clip(noisy_context, 0, 1)
            
            augmented_sample['context_features'] = noisy_context
        
        return augmented_sample
    
    def sign_rotation_augmentation(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply sign rotation while preserving astrological relationships
        """
        if random.random() > self.config.sign_rotation_prob:
            return sample
        
        if not self.config.preserve_core_relationships:
            return sample
        
        augmented_sample = copy.deepcopy(sample)
        
        # Get original signs
        sign1_idx = augmented_sample.get('sign1_idx', 0)
        sign2_idx = augmented_sample.get('sign2_idx', 0)
        
        # Find signs in the same element/modality group
        original_element1 = self._get_element(sign1_idx)
        original_element2 = self._get_element(sign2_idx)
        
        # Rotate within same element group to preserve relationships
        if original_element1:
            available_signs1 = self.element_groups[original_element1]
            new_sign1 = random.choice([s for s in available_signs1 if s != sign1_idx])
            augmented_sample['sign1_idx'] = new_sign1
        
        if original_element2:
            available_signs2 = self.element_groups[original_element2]
            new_sign2 = random.choice([s for s in available_signs2 if s != sign2_idx])
            augmented_sample['sign2_idx'] = new_sign2
        
        # Adjust compatibility scores based on new sign combination
        if 'targets' in augmented_sample:
            new_sign1 = augmented_sample['sign1_idx']
            new_sign2 = augmented_sample['sign2_idx']
            
            # Apply compatibility weight adjustment
            compatibility_modifier = self.compatibility_weights[new_sign1, new_sign2]
            targets = np.array(augmented_sample['targets'])
            targets = np.clip(targets * compatibility_modifier, 0, 1)
            augmented_sample['targets'] = targets
        
        return augmented_sample
    
    def aspect_perturbation(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        """Add small perturbations to aspect matrix"""
        if random.random() > self.config.aspect_perturbation_prob:
            return sample
        
        augmented_sample = copy.deepcopy(sample)
        
        if 'aspect_matrix' in augmented_sample:
            aspect_matrix = np.array(augmented_sample['aspect_matrix'])
            
            # Add small random perturbations
            noise = np.random.normal(0, self.config.aspect_perturbation_std, aspect_matrix.shape)
            perturbed_matrix = aspect_matrix + noise
            
            # Ensure matrix remains positive and bounded
            perturbed_matrix = np.clip(perturbed_matrix, 0, 1)
            
            augmented_sample['aspect_matrix'] = perturbed_matrix
        
        return augmented_sample
    
    def compatibility_scaling(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        """Apply slight scaling to compatibility scores"""
        if random.random() > self.config.compatibility_scaling_prob:
            return sample
        
        augmented_sample = copy.deepcopy(sample)
        
        if 'targets' in augmented_sample:
            targets = np.array(augmented_sample['targets'])
            
            # Apply random scaling
            scale_factor = random.uniform(*self.config.compatibility_scaling_range)
            scaled_targets = targets * scale_factor
            
            # Ensure values remain in [0, 1]
            scaled_targets = np.clip(scaled_targets, 0, 1)
            
            augmented_sample['targets'] = scaled_targets
        
        return augmented_sample
    
    def seasonal_variation(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        """Apply seasonal variations to compatibility"""
        if random.random() > self.config.seasonal_variation_prob:
            return sample
        
        augmented_sample = copy.deepcopy(sample)
        
        # Simulate seasonal effects
        season = random.choice(['spring', 'summer', 'autumn', 'winter'])
        
        # Different elements are stronger in different seasons
        seasonal_modifiers = {
            'spring': {'fire': 1.1, 'earth': 0.95, 'air': 1.05, 'water': 1.0},
            'summer': {'fire': 1.15, 'earth': 0.9, 'air': 1.0, 'water': 0.95},
            'autumn': {'fire': 0.95, 'earth': 1.1, 'air': 1.0, 'water': 1.05},
            'winter': {'fire': 0.9, 'earth': 1.05, 'air': 0.95, 'water': 1.15}
        }
        
        if 'targets' in augmented_sample:
            sign1_idx = augmented_sample.get('sign1_idx', 0)
            sign2_idx = augmented_sample.get('sign2_idx', 0)
            
            element1 = self._get_element(sign1_idx)
            element2 = self._get_element(sign2_idx)
            
            if element1 and element2:
                modifier1 = seasonal_modifiers[season][element1]
                modifier2 = seasonal_modifiers[season][element2]
                avg_modifier = (modifier1 + modifier2) / 2
                
                targets = np.array(augmented_sample['targets'])
                targets = np.clip(targets * avg_modifier, 0, 1)
                augmented_sample['targets'] = targets
        
        return augmented_sample
    
    def moon_phase_variation(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        """Apply moon phase variations"""
        if random.random() > self.config.moon_phase_prob:
            return sample
        
        augmented_sample = copy.deepcopy(sample)
        
        # Moon phases affect emotional and intuitive compatibility
        moon_phases = ['new', 'waxing', 'full', 'waning']
        current_phase = random.choice(moon_phases)
        
        # Full moon enhances emotional connections, new moon enhances fresh starts
        phase_effects = {
            'new': {'emotional': 0.95, 'spiritual': 1.05, 'overall': 1.0},
            'waxing': {'love': 1.05, 'trust': 1.05, 'overall': 1.02},
            'full': {'emotional': 1.1, 'physical': 1.05, 'overall': 1.05},
            'waning': {'intellectual': 1.05, 'values': 1.05, 'overall': 0.98}
        }
        
        if 'targets' in augmented_sample:
            targets = np.array(augmented_sample['targets'])
            effects = phase_effects[current_phase]
            
            # Apply dimensional effects (assuming target order matches dimensions)
            dimension_names = ['love', 'friendship', 'communication', 'emotional',
                             'intellectual', 'physical', 'spiritual', 'career',
                             'family', 'trust', 'values', 'overall']
            
            for i, dim in enumerate(dimension_names):
                if i < len(targets) and dim in effects:
                    targets[i] *= effects[dim]
            
            targets = np.clip(targets, 0, 1)
            augmented_sample['targets'] = targets
        
        return augmented_sample
    
    def planetary_retrograde_effect(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        """Apply planetary retrograde effects"""
        if random.random() > self.config.retrograde_prob:
            return sample
        
        augmented_sample = copy.deepcopy(sample)
        
        # Mercury retrograde affects communication
        # Venus retrograde affects love relationships
        retrograde_effects = {
            'mercury': {'communication': 0.9, 'intellectual': 0.95},
            'venus': {'love': 0.9, 'physical': 0.95, 'values': 0.92},
            'mars': {'physical': 0.85, 'career': 0.9}
        }
        
        retrograde_planet = random.choice(list(retrograde_effects.keys()))
        effects = retrograde_effects[retrograde_planet]
        
        if 'targets' in augmented_sample:
            targets = np.array(augmented_sample['targets'])
            
            # Apply retrograde effects
            dimension_names = ['love', 'friendship', 'communication', 'emotional',
                             'intellectual', 'physical', 'spiritual', 'career',
                             'family', 'trust', 'values', 'overall']
            
            for i, dim in enumerate(dimension_names):
                if i < len(targets) and dim in effects:
                    targets[i] *= effects[dim]
            
            targets = np.clip(targets, 0, 1)
            augmented_sample['targets'] = targets
        
        return augmented_sample
    
    def _get_element(self, sign_idx: int) -> Optional[str]:
        """Get element for a zodiac sign"""
        for element, signs in self.element_groups.items():
            if sign_idx in signs:
                return element
        return None
    
    def _get_modality(self, sign_idx: int) -> Optional[str]:
        """Get modality for a zodiac sign"""
        for modality, signs in self.modality_groups.items():
            if sign_idx in signs:
                return modality
        return None


class AdvancedCompatibilityAugmentation:
    """
    Advanced augmentation techniques for neural compatibility training
    """
    
    def __init__(self):
        self.base_augmenter = CompatibilityDataAugmentation()
        
    def mixup_augmentation(self, batch1: Dict[str, torch.Tensor], 
                          batch2: Dict[str, torch.Tensor], 
                          alpha: float = 0.2) -> Dict[str, torch.Tensor]:
        """
        Apply MixUp augmentation for compatibility data
        """
        # Sample lambda from Beta distribution
        lam = np.random.beta(alpha, alpha)
        
        mixed_batch = {}
        
        # Mix numerical features
        for key in ['aspect_matrix', 'context_features', 'targets']:
            if key in batch1 and key in batch2:
                mixed_batch[key] = lam * batch1[key] + (1 - lam) * batch2[key]
        
        # For categorical features (signs), choose based on lambda
        for key in ['sign1_idx', 'sign2_idx']:
            if key in batch1 and key in batch2:
                mask = torch.rand(batch1[key].shape) < lam
                mixed_batch[key] = torch.where(mask, batch1[key], batch2[key])
        
        return mixed_batch
    
    def cutmix_augmentation(self, batch1: Dict[str, torch.Tensor], 
                           batch2: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        """
        Apply CutMix augmentation for aspect matrices
        """
        mixed_batch = copy.deepcopy(batch1)
        
        if 'aspect_matrix' in batch1 and 'aspect_matrix' in batch2:
            # Random crop parameters
            h, w = batch1['aspect_matrix'].shape[-2:]
            cut_ratio = np.random.uniform(0.2, 0.5)
            cut_h, cut_w = int(h * cut_ratio), int(w * cut_ratio)
            
            # Random position
            start_h = np.random.randint(0, h - cut_h + 1)
            start_w = np.random.randint(0, w - cut_w + 1)
            
            # Apply cut and mix
            mixed_batch['aspect_matrix'][..., start_h:start_h+cut_h, start_w:start_w+cut_w] = \
                batch2['aspect_matrix'][..., start_h:start_h+cut_h, start_w:start_w+cut_w]
            
            # Adjust labels proportionally
            lam = 1 - (cut_h * cut_w) / (h * w)
            mixed_batch['targets'] = lam * batch1['targets'] + (1 - lam) * batch2['targets']
        
        return mixed_batch
    
    def gaussian_augmentation(self, sample: Dict[str, Any], 
                            noise_level: float = 0.01) -> Dict[str, Any]:
        """
        Apply Gaussian noise augmentation
        """
        augmented_sample = copy.deepcopy(sample)
        
        # Add noise to continuous features
        for key in ['aspect_matrix', 'context_features']:
            if key in augmented_sample:
                data = augmented_sample[key]
                if isinstance(data, np.ndarray):
                    noise = np.random.normal(0, noise_level, data.shape)
                    augmented_sample[key] = np.clip(data + noise, 0, 1)
                elif torch.is_tensor(data):
                    noise = torch.normal(0, noise_level, data.shape)
                    augmented_sample[key] = torch.clamp(data + noise, 0, 1)
        
        return augmented_sample


# Augmentation pipeline for training
class AugmentationPipeline:
    """
    Complete augmentation pipeline for training data
    """
    
    def __init__(self, config: CompatibilityAugmentationConfig = None):
        self.config = config or CompatibilityAugmentationConfig()
        self.basic_augmenter = CompatibilityDataAugmentation(self.config)
        self.advanced_augmenter = AdvancedCompatibilityAugmentation()
        
    def __call__(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        """Apply augmentation pipeline to a sample"""
        # Apply basic augmentations
        augmented_sample = self.basic_augmenter._augment_single_sample(sample)
        
        # Apply advanced augmentations with probability
        if random.random() < 0.2:  # 20% chance for Gaussian augmentation
            augmented_sample = self.advanced_augmenter.gaussian_augmentation(augmented_sample)
        
        return augmented_sample
    
    def augment_batch(self, batch: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        """Apply batch-level augmentations (MixUp, CutMix)"""
        if random.random() < 0.3:  # 30% chance for batch augmentation
            # Get another batch for mixing
            batch_size = batch[list(batch.keys())[0]].size(0)
            indices = torch.randperm(batch_size)
            shuffled_batch = {k: v[indices] for k, v in batch.items()}
            
            if random.random() < 0.5:  # MixUp
                return self.advanced_augmenter.mixup_augmentation(batch, shuffled_batch)
            else:  # CutMix
                return self.advanced_augmenter.cutmix_augmentation(batch, shuffled_batch)
        
        return batch


if __name__ == "__main__":
    # Test augmentation pipeline
    config = CompatibilityAugmentationConfig()
    augmenter = CompatibilityDataAugmentation(config)
    
    # Create a sample data point
    sample = {
        'sign1_idx': 0,  # Aries
        'sign2_idx': 4,  # Leo
        'aspect_matrix': np.random.rand(12, 12),
        'context_features': np.random.rand(50),
        'targets': np.random.rand(12),
        'temporal_context': [12, 15, 6, 2024]  # hour, day, month, year
    }
    
    # Test augmentation
    augmented_sample = augmenter._augment_single_sample(sample)
    print(f"Original sign1: {sample['sign1_idx']}, Augmented sign1: {augmented_sample['sign1_idx']}")
    print(f"Original targets mean: {np.mean(sample['targets']):.3f}, "
          f"Augmented targets mean: {np.mean(augmented_sample['targets']):.3f}")
    
    # Test dataset augmentation
    dataset = [sample] * 5
    augmented_dataset = augmenter.augment_dataset(dataset, augmentation_factor=2)
    print(f"Original dataset size: {len(dataset)}, Augmented size: {len(augmented_dataset)}")
    
    # Test pipeline
    pipeline = AugmentationPipeline(config)
    pipeline_result = pipeline(sample)
    print("Augmentation pipeline test completed successfully!")