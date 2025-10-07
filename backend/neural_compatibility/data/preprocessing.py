import torch
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass
import json
import pickle
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.decomposition import PCA
import logging
from datetime import datetime, timezone
import pytz

@dataclass
class PreprocessingConfig:
    """Configuration for data preprocessing"""
    # Normalization settings
    normalize_features: bool = True
    normalization_method: str = 'minmax'  # 'minmax', 'standard', 'robust'
    
    # Feature engineering settings
    create_interaction_features: bool = True
    apply_pca: bool = False
    pca_components: int = 50
    
    # Temporal processing
    include_temporal_features: bool = True
    timezone_normalization: bool = True
    
    # Astrological feature engineering
    calculate_aspects: bool = True
    include_house_positions: bool = True
    add_element_modality_features: bool = True
    
    # Missing data handling
    handle_missing_data: bool = True
    missing_strategy: str = 'astrological_mean'  # 'mean', 'median', 'astrological_mean'
    
    # Validation
    validate_astrological_consistency: bool = True


class CompatibilityPreprocessor:
    """
    Comprehensive preprocessor for zodiac compatibility data
    Handles feature engineering, normalization, and astrological calculations
    """
    
    def __init__(self, config: PreprocessingConfig = None):
        self.config = config or PreprocessingConfig()
        self.is_fitted = False
        
        # Scalers for different feature types
        self.scalers = {}
        self.label_encoders = {}
        self.pca_transformer = None
        
        # Astrological knowledge
        self._initialize_astrological_data()
        
        # Statistics for preprocessing
        self.feature_stats = {}
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
    
    def _initialize_astrological_data(self):
        """Initialize astrological reference data"""
        # Zodiac sign properties
        self.sign_properties = {
            0: {'name': 'Aries', 'element': 'fire', 'modality': 'cardinal', 'ruler': 'mars', 'house': 1},
            1: {'name': 'Taurus', 'element': 'earth', 'modality': 'fixed', 'ruler': 'venus', 'house': 2},
            2: {'name': 'Gemini', 'element': 'air', 'modality': 'mutable', 'ruler': 'mercury', 'house': 3},
            3: {'name': 'Cancer', 'element': 'water', 'modality': 'cardinal', 'ruler': 'moon', 'house': 4},
            4: {'name': 'Leo', 'element': 'fire', 'modality': 'fixed', 'ruler': 'sun', 'house': 5},
            5: {'name': 'Virgo', 'element': 'earth', 'modality': 'mutable', 'ruler': 'mercury', 'house': 6},
            6: {'name': 'Libra', 'element': 'air', 'modality': 'cardinal', 'ruler': 'venus', 'house': 7},
            7: {'name': 'Scorpio', 'element': 'water', 'modality': 'fixed', 'ruler': 'pluto', 'house': 8},
            8: {'name': 'Sagittarius', 'element': 'fire', 'modality': 'mutable', 'ruler': 'jupiter', 'house': 9},
            9: {'name': 'Capricorn', 'element': 'earth', 'modality': 'cardinal', 'ruler': 'saturn', 'house': 10},
            10: {'name': 'Aquarius', 'element': 'air', 'modality': 'fixed', 'ruler': 'uranus', 'house': 11},
            11: {'name': 'Pisces', 'element': 'water', 'modality': 'mutable', 'ruler': 'neptune', 'house': 12}
        }
        
        # Element compatibility matrix
        self.element_compatibility = {
            ('fire', 'fire'): 0.8, ('fire', 'earth'): 0.3, ('fire', 'air'): 0.9, ('fire', 'water'): 0.3,
            ('earth', 'fire'): 0.3, ('earth', 'earth'): 0.8, ('earth', 'air'): 0.3, ('earth', 'water'): 0.9,
            ('air', 'fire'): 0.9, ('air', 'earth'): 0.3, ('air', 'air'): 0.8, ('air', 'water'): 0.3,
            ('water', 'fire'): 0.3, ('water', 'earth'): 0.9, ('water', 'air'): 0.3, ('water', 'water'): 0.8
        }
        
        # Aspect angles and their meanings
        self.aspects = {
            0: {'name': 'conjunction', 'angle': 0, 'strength': 1.0, 'nature': 'neutral'},
            1: {'name': 'sextile', 'angle': 60, 'strength': 0.6, 'nature': 'harmonious'},
            2: {'name': 'square', 'angle': 90, 'strength': 0.8, 'nature': 'challenging'},
            3: {'name': 'trine', 'angle': 120, 'strength': 0.9, 'nature': 'harmonious'},
            4: {'name': 'opposition', 'angle': 180, 'strength': 0.9, 'nature': 'challenging'},
            5: {'name': 'quincunx', 'angle': 150, 'strength': 0.4, 'nature': 'neutral'}
        }
        
        # Traditional compatibility scores by sign combination
        self.traditional_compatibility = self._calculate_traditional_compatibility_matrix()
    
    def _calculate_traditional_compatibility_matrix(self) -> np.ndarray:
        """Calculate traditional compatibility matrix based on astrological rules"""
        matrix = np.zeros((12, 12))
        
        for i in range(12):
            for j in range(12):
                if i == j:
                    matrix[i, j] = 0.7  # Same sign compatibility
                else:
                    elem1 = self.sign_properties[i]['element']
                    elem2 = self.sign_properties[j]['element']
                    
                    base_compatibility = self.element_compatibility.get((elem1, elem2), 0.5)
                    
                    # Adjust for aspect relationship
                    angle_diff = abs(i - j) * 30  # Each sign is 30 degrees apart
                    angle_diff = min(angle_diff, 360 - angle_diff)  # Handle wrap-around
                    
                    aspect_modifier = 1.0
                    if 55 <= angle_diff <= 65:  # Sextile (60°)
                        aspect_modifier = 1.2
                    elif 115 <= angle_diff <= 125:  # Trine (120°)
                        aspect_modifier = 1.3
                    elif 85 <= angle_diff <= 95:  # Square (90°)
                        aspect_modifier = 0.8
                    elif 175 <= angle_diff <= 185:  # Opposition (180°)
                        aspect_modifier = 0.7
                    
                    matrix[i, j] = base_compatibility * aspect_modifier
        
        return matrix
    
    def fit(self, raw_data: List[Dict[str, Any]]) -> 'CompatibilityPreprocessor':
        """
        Fit the preprocessor on raw data
        
        Args:
            raw_data: List of raw compatibility data samples
            
        Returns:
            Fitted preprocessor
        """
        self.logger.info("Fitting compatibility preprocessor...")
        
        # Convert raw data to structured format
        structured_data = self._structure_raw_data(raw_data)
        
        # Extract features for fitting scalers
        if self.config.normalize_features:
            self._fit_scalers(structured_data)
        
        # Fit PCA if required
        if self.config.apply_pca:
            self._fit_pca(structured_data)
        
        # Calculate feature statistics
        self._calculate_feature_stats(structured_data)
        
        self.is_fitted = True
        self.logger.info("Preprocessor fitting completed")
        
        return self
    
    def transform(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Transform raw data using fitted preprocessor
        
        Args:
            raw_data: List of raw compatibility data samples
            
        Returns:
            List of preprocessed samples
        """
        if not self.is_fitted:
            raise ValueError("Preprocessor must be fitted before transform")
        
        self.logger.info(f"Transforming {len(raw_data)} samples...")
        
        # Structure raw data
        structured_data = self._structure_raw_data(raw_data)
        
        # Apply preprocessing steps
        processed_data = []
        for sample in structured_data:
            processed_sample = self._transform_single_sample(sample)
            processed_data.append(processed_sample)
        
        self.logger.info("Data transformation completed")
        
        return processed_data
    
    def fit_transform(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Fit preprocessor and transform data in one step"""
        return self.fit(raw_data).transform(raw_data)
    
    def _structure_raw_data(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert raw data to structured format"""
        structured_data = []
        
        for sample in raw_data:
            structured_sample = {
                'sign1_idx': self._process_sign_input(sample.get('sign1', sample.get('person1_sign', 0))),
                'sign2_idx': self._process_sign_input(sample.get('sign2', sample.get('person2_sign', 0))),
                'birth_data1': sample.get('birth_data1', {}),
                'birth_data2': sample.get('birth_data2', {}),
                'context_info': sample.get('context', {}),
                'compatibility_scores': sample.get('compatibility_scores', sample.get('targets', {})),
                'metadata': sample.get('metadata', {})
            }
            
            structured_data.append(structured_sample)
        
        return structured_data
    
    def _process_sign_input(self, sign_input: Union[str, int, Dict[str, Any]]) -> int:
        """Convert various sign input formats to sign index"""
        if isinstance(sign_input, int):
            return max(0, min(11, sign_input))  # Ensure valid range
        elif isinstance(sign_input, str):
            # Map sign names to indices
            sign_map = {
                'aries': 0, 'taurus': 1, 'gemini': 2, 'cancer': 3,
                'leo': 4, 'virgo': 5, 'libra': 6, 'scorpio': 7,
                'sagittarius': 8, 'capricorn': 9, 'aquarius': 10, 'pisces': 11
            }
            return sign_map.get(sign_input.lower(), 0)
        elif isinstance(sign_input, dict) and 'sign' in sign_input:
            return self._process_sign_input(sign_input['sign'])
        else:
            return 0  # Default to Aries
    
    def _transform_single_sample(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        """Transform a single sample"""
        processed_sample = {}
        
        # Basic sign information
        processed_sample['sign1_idx'] = sample['sign1_idx']
        processed_sample['sign2_idx'] = sample['sign2_idx']
        
        # Generate aspect matrix
        processed_sample['aspect_matrix'] = self._generate_aspect_matrix(
            sample['sign1_idx'], sample['sign2_idx']
        )
        
        # Create context features
        processed_sample['context_features'] = self._create_context_features(sample)
        
        # Process targets
        processed_sample['targets'] = self._process_targets(sample)
        
        # Add temporal features if available
        if self.config.include_temporal_features:
            processed_sample['temporal_context'] = self._extract_temporal_features(sample)
        
        # Add engineered features
        if self.config.create_interaction_features:
            processed_sample.update(self._create_interaction_features(sample))
        
        return processed_sample
    
    def _generate_aspect_matrix(self, sign1_idx: int, sign2_idx: int) -> np.ndarray:
        """Generate aspect matrix for sign pair"""
        matrix = np.zeros((12, 12))
        
        # Calculate aspects between all combinations
        for i in range(12):
            for j in range(12):
                angle_diff = abs(i - j) * 30
                angle_diff = min(angle_diff, 360 - angle_diff)
                
                # Find closest aspect
                aspect_strength = 0.0
                for aspect_info in self.aspects.values():
                    if abs(angle_diff - aspect_info['angle']) <= 8:  # 8-degree orb
                        aspect_strength = aspect_info['strength']
                        break
                
                matrix[i, j] = aspect_strength
        
        # Emphasize the actual sign combination
        matrix[sign1_idx, sign2_idx] = self.traditional_compatibility[sign1_idx, sign2_idx]
        matrix[sign2_idx, sign1_idx] = self.traditional_compatibility[sign2_idx, sign1_idx]
        
        return matrix
    
    def _create_context_features(self, sample: Dict[str, Any]) -> np.ndarray:
        """Create context feature vector"""
        features = []
        
        # Sign properties for both signs
        for sign_idx in [sample['sign1_idx'], sample['sign2_idx']]:
            props = self.sign_properties[sign_idx]
            
            # Element encoding (one-hot)
            element_vector = [0, 0, 0, 0]  # fire, earth, air, water
            element_map = {'fire': 0, 'earth': 1, 'air': 2, 'water': 3}
            element_vector[element_map[props['element']]] = 1
            features.extend(element_vector)
            
            # Modality encoding (one-hot)
            modality_vector = [0, 0, 0]  # cardinal, fixed, mutable
            modality_map = {'cardinal': 0, 'fixed': 1, 'mutable': 2}
            modality_vector[modality_map[props['modality']]] = 1
            features.extend(modality_vector)
            
            # House number (normalized)
            features.append(props['house'] / 12.0)
        
        # Compatibility features
        elem1 = self.sign_properties[sample['sign1_idx']]['element']
        elem2 = self.sign_properties[sample['sign2_idx']]['element']
        features.append(self.element_compatibility.get((elem1, elem2), 0.5))
        
        # Traditional compatibility score
        features.append(self.traditional_compatibility[sample['sign1_idx'], sample['sign2_idx']])
        
        # Angular relationship
        angle_diff = abs(sample['sign1_idx'] - sample['sign2_idx']) * 30
        angle_diff = min(angle_diff, 360 - angle_diff)
        features.append(angle_diff / 180.0)  # Normalize to [0, 1]
        
        # Birth data features (if available)
        birth_features = self._extract_birth_features(sample)
        features.extend(birth_features)
        
        # Context information
        context_features = self._extract_context_info_features(sample)
        features.extend(context_features)
        
        # Pad to fixed size (50 features)
        while len(features) < 50:
            features.append(0.0)
        
        feature_array = np.array(features[:50])  # Truncate if too long
        
        # Apply normalization if fitted
        if self.config.normalize_features and 'context_features' in self.scalers:
            feature_array = self.scalers['context_features'].transform(
                feature_array.reshape(1, -1)
            ).flatten()
        
        return feature_array
    
    def _extract_birth_features(self, sample: Dict[str, Any]) -> List[float]:
        """Extract features from birth data"""
        features = []
        
        for birth_key in ['birth_data1', 'birth_data2']:
            birth_data = sample.get(birth_key, {})
            
            # Time features (normalized)
            hour = birth_data.get('hour', 12) / 24.0
            day = birth_data.get('day', 15) / 31.0
            month = birth_data.get('month', 6) / 12.0
            features.extend([hour, day, month])
            
            # Location features (if available)
            latitude = birth_data.get('latitude', 0) / 90.0  # Normalize to [-1, 1]
            longitude = birth_data.get('longitude', 0) / 180.0
            features.extend([latitude, longitude])
        
        return features
    
    def _extract_context_info_features(self, sample: Dict[str, Any]) -> List[float]:
        """Extract features from context information"""
        context = sample.get('context_info', {})
        features = []
        
        # Relationship type encoding
        rel_type = context.get('relationship_type', 'romantic')
        rel_encoding = {'romantic': [1, 0, 0], 'friendship': [0, 1, 0], 'business': [0, 0, 1]}
        features.extend(rel_encoding.get(rel_type, [0, 0, 0]))
        
        # Duration of relationship (normalized months)
        duration = context.get('duration_months', 0)
        features.append(min(duration / 120.0, 1.0))  # Cap at 10 years
        
        # Age difference (normalized)
        age_diff = abs(context.get('age_difference', 0))
        features.append(min(age_diff / 30.0, 1.0))  # Cap at 30 years
        
        return features
    
    def _extract_temporal_features(self, sample: Dict[str, Any]) -> np.ndarray:
        """Extract temporal context features"""
        temporal_features = []
        
        # Current time context
        now = datetime.now()
        
        # Time-based features
        temporal_features.extend([
            now.hour / 24.0,
            now.day / 31.0,
            now.month / 12.0,
            (now.year % 100) / 100.0  # Normalize year to century
        ])
        
        # Seasonal features
        season_encoding = [0, 0, 0, 0]  # spring, summer, autumn, winter
        month = now.month
        if 3 <= month <= 5:
            season_encoding[0] = 1  # spring
        elif 6 <= month <= 8:
            season_encoding[1] = 1  # summer
        elif 9 <= month <= 11:
            season_encoding[2] = 1  # autumn
        else:
            season_encoding[3] = 1  # winter
        
        temporal_features.extend(season_encoding)
        
        return np.array(temporal_features)
    
    def _create_interaction_features(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        """Create interaction features between signs"""
        sign1_idx = sample['sign1_idx']
        sign2_idx = sample['sign2_idx']
        
        interaction_features = {}
        
        # Element interaction
        elem1 = self.sign_properties[sign1_idx]['element']
        elem2 = self.sign_properties[sign2_idx]['element']
        interaction_features['element_harmony'] = self.element_compatibility.get((elem1, elem2), 0.5)
        
        # Modality interaction
        mod1 = self.sign_properties[sign1_idx]['modality']
        mod2 = self.sign_properties[sign2_idx]['modality']
        interaction_features['modality_match'] = 1.0 if mod1 == mod2 else 0.0
        
        # House distance
        house1 = self.sign_properties[sign1_idx]['house']
        house2 = self.sign_properties[sign2_idx]['house']
        house_distance = min(abs(house1 - house2), 12 - abs(house1 - house2))
        interaction_features['house_distance_norm'] = house_distance / 6.0
        
        return interaction_features
    
    def _process_targets(self, sample: Dict[str, Any]) -> np.ndarray:
        """Process compatibility score targets"""
        scores = sample.get('compatibility_scores', {})
        
        # Dimension names in order
        dimensions = ['love', 'friendship', 'communication', 'emotional', 
                     'intellectual', 'physical', 'spiritual', 'career',
                     'family', 'trust', 'values', 'overall']
        
        target_vector = []
        for dim in dimensions:
            if isinstance(scores, dict):
                score = scores.get(dim, 0.5)  # Default to neutral
            elif isinstance(scores, (list, np.ndarray)) and len(scores) >= len(target_vector) + 1:
                score = scores[len(target_vector)]
            else:
                score = 0.5
            
            # Ensure score is in valid range [0, 1]
            target_vector.append(max(0.0, min(1.0, float(score))))
        
        return np.array(target_vector)
    
    def _fit_scalers(self, structured_data: List[Dict[str, Any]]):
        """Fit scalers on structured data"""
        # Extract features for fitting
        context_features = []
        
        for sample in structured_data:
            processed_sample = {
                'sign1_idx': sample['sign1_idx'],
                'sign2_idx': sample['sign2_idx'],
                'birth_data1': sample['birth_data1'],
                'birth_data2': sample['birth_data2'],
                'context_info': sample['context_info']
            }
            context_feat = self._create_context_features(processed_sample)
            context_features.append(context_feat)
        
        # Fit scaler for context features
        context_array = np.array(context_features)
        
        if self.config.normalization_method == 'minmax':
            self.scalers['context_features'] = MinMaxScaler()
        elif self.config.normalization_method == 'standard':
            self.scalers['context_features'] = StandardScaler()
        
        self.scalers['context_features'].fit(context_array)
    
    def _fit_pca(self, structured_data: List[Dict[str, Any]]):
        """Fit PCA transformer"""
        if not self.config.apply_pca:
            return
        
        # Extract high-dimensional features for PCA
        features_for_pca = []
        
        for sample in structured_data:
            # Use context features as input for PCA
            processed_sample = {
                'sign1_idx': sample['sign1_idx'],
                'sign2_idx': sample['sign2_idx'],
                'birth_data1': sample['birth_data1'],
                'birth_data2': sample['birth_data2'],
                'context_info': sample['context_info']
            }
            context_feat = self._create_context_features(processed_sample)
            features_for_pca.append(context_feat)
        
        feature_array = np.array(features_for_pca)
        
        self.pca_transformer = PCA(n_components=self.config.pca_components)
        self.pca_transformer.fit(feature_array)
    
    def _calculate_feature_stats(self, structured_data: List[Dict[str, Any]]):
        """Calculate feature statistics for validation"""
        sign1_counts = {}
        sign2_counts = {}
        
        for sample in structured_data:
            sign1 = sample['sign1_idx']
            sign2 = sample['sign2_idx']
            
            sign1_counts[sign1] = sign1_counts.get(sign1, 0) + 1
            sign2_counts[sign2] = sign2_counts.get(sign2, 0) + 1
        
        self.feature_stats = {
            'total_samples': len(structured_data),
            'sign1_distribution': sign1_counts,
            'sign2_distribution': sign2_counts,
            'unique_sign1_count': len(sign1_counts),
            'unique_sign2_count': len(sign2_counts)
        }
    
    def save(self, filepath: str):
        """Save fitted preprocessor to file"""
        if not self.is_fitted:
            raise ValueError("Cannot save unfitted preprocessor")
        
        save_data = {
            'config': self.config,
            'scalers': self.scalers,
            'pca_transformer': self.pca_transformer,
            'feature_stats': self.feature_stats,
            'is_fitted': self.is_fitted,
            'sign_properties': self.sign_properties,
            'element_compatibility': self.element_compatibility,
            'traditional_compatibility': self.traditional_compatibility
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(save_data, f)
        
        self.logger.info(f"Preprocessor saved to {filepath}")
    
    @classmethod
    def load(cls, filepath: str) -> 'CompatibilityPreprocessor':
        """Load fitted preprocessor from file"""
        with open(filepath, 'rb') as f:
            save_data = pickle.load(f)
        
        preprocessor = cls(save_data['config'])
        preprocessor.scalers = save_data['scalers']
        preprocessor.pca_transformer = save_data['pca_transformer']
        preprocessor.feature_stats = save_data['feature_stats']
        preprocessor.is_fitted = save_data['is_fitted']
        preprocessor.sign_properties = save_data['sign_properties']
        preprocessor.element_compatibility = save_data['element_compatibility']
        preprocessor.traditional_compatibility = save_data['traditional_compatibility']
        
        return preprocessor
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Calculate feature importance based on astrological knowledge"""
        importance = {
            'sign_indices': 0.25,
            'element_compatibility': 0.20,
            'aspect_relationships': 0.15,
            'traditional_compatibility': 0.15,
            'temporal_context': 0.10,
            'birth_data': 0.08,
            'context_info': 0.07
        }
        
        return importance


if __name__ == "__main__":
    # Test preprocessing pipeline
    config = PreprocessingConfig()
    preprocessor = CompatibilityPreprocessor(config)
    
    # Create sample raw data
    raw_data = [
        {
            'sign1': 'aries',
            'sign2': 'leo',
            'birth_data1': {'hour': 10, 'day': 15, 'month': 4, 'latitude': 40.7, 'longitude': -74.0},
            'birth_data2': {'hour': 14, 'day': 23, 'month': 8, 'latitude': 34.0, 'longitude': -118.2},
            'context': {'relationship_type': 'romantic', 'duration_months': 6, 'age_difference': 3},
            'compatibility_scores': {
                'love': 0.85, 'friendship': 0.78, 'communication': 0.82,
                'emotional': 0.75, 'intellectual': 0.73, 'physical': 0.88,
                'spiritual': 0.70, 'career': 0.65, 'family': 0.72,
                'trust': 0.80, 'values': 0.76, 'overall': 0.77
            }
        },
        {
            'sign1': 2,  # Gemini
            'sign2': 6,  # Libra
            'compatibility_scores': [0.75, 0.82, 0.90, 0.68, 0.95, 0.65, 0.73, 0.78, 0.70, 0.85, 0.80, 0.77]
        }
    ]
    
    # Test fit and transform
    processed_data = preprocessor.fit_transform(raw_data)
    
    print(f"Processed {len(processed_data)} samples")
    print(f"Sample keys: {list(processed_data[0].keys())}")
    print(f"Context features shape: {processed_data[0]['context_features'].shape}")
    print(f"Aspect matrix shape: {processed_data[0]['aspect_matrix'].shape}")
    print(f"Targets shape: {processed_data[0]['targets'].shape}")
    print(f"Feature stats: {preprocessor.feature_stats}")
    
    # Test save/load
    preprocessor.save('test_preprocessor.pkl')
    loaded_preprocessor = CompatibilityPreprocessor.load('test_preprocessor.pkl')
    print("Save/load test successful!")
    
    # Test feature importance
    importance = preprocessor.get_feature_importance()
    print(f"Feature importance: {importance}")
    
    print("Preprocessing pipeline test completed successfully!")