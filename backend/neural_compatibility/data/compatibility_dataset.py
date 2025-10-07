import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
import pandas as pd
import json
import os
from typing import Dict, List, Tuple, Optional, Any, Union
import logging
from pathlib import Path
import random

from .preprocessing import CompatibilityPreprocessor, PreprocessingConfig
from .augmentation import CompatibilityDataAugmentation, CompatibilityAugmentationConfig, AugmentationPipeline

class CompatibilityDataset(Dataset):
    """
    PyTorch Dataset for zodiac compatibility data
    Handles loading, preprocessing, and augmentation
    """
    
    def __init__(self, data_path: str, 
                 preprocessor: Optional[CompatibilityPreprocessor] = None,
                 augment: bool = False,
                 augmentation_factor: int = 3,
                 split: str = 'train',
                 cache_processed: bool = True):
        """
        Initialize compatibility dataset
        
        Args:
            data_path: Path to data directory or file
            preprocessor: Optional preprocessor instance
            augment: Whether to apply data augmentation
            augmentation_factor: Number of augmented samples per original
            split: Dataset split ('train', 'val', 'test')
            cache_processed: Whether to cache processed data
        """
        self.data_path = Path(data_path)
        self.split = split
        self.augment = augment
        self.augmentation_factor = augmentation_factor
        self.cache_processed = cache_processed
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Initialize preprocessor
        if preprocessor is None:
            self.preprocessor = CompatibilityPreprocessor()
        else:
            self.preprocessor = preprocessor
        
        # Initialize augmentation pipeline
        if self.augment:
            aug_config = CompatibilityAugmentationConfig()
            self.augmentation_pipeline = AugmentationPipeline(aug_config)
        else:
            self.augmentation_pipeline = None
        
        # Load and preprocess data
        self.data = self._load_and_preprocess_data()
        
        # Cache path for processed data
        if self.cache_processed:
            cache_dir = self.data_path.parent / 'cache'
            cache_dir.mkdir(exist_ok=True)
            self.cache_path = cache_dir / f'{self.split}_processed.pt'
        
        self.logger.info(f"Initialized dataset with {len(self.data)} samples")
    
    def _load_and_preprocess_data(self) -> List[Dict[str, torch.Tensor]]:
        """Load raw data and preprocess it"""
        
        # Try to load from cache first
        if self.cache_processed and hasattr(self, 'cache_path') and self.cache_path.exists():
            self.logger.info(f"Loading cached data from {self.cache_path}")
            return torch.load(self.cache_path)
        
        # Load raw data
        raw_data = self._load_raw_data()
        
        # Fit preprocessor on training data
        if self.split == 'train' and not self.preprocessor.is_fitted:
            self.logger.info("Fitting preprocessor on training data")
            self.preprocessor.fit(raw_data)
        
        # Transform data
        self.logger.info("Preprocessing data...")
        processed_raw_data = self.preprocessor.transform(raw_data)
        
        # Apply augmentation if enabled
        if self.augment and self.split == 'train':
            self.logger.info(f"Applying data augmentation with factor {self.augmentation_factor}")
            augmenter = CompatibilityDataAugmentation()
            processed_raw_data = augmenter.augment_dataset(
                processed_raw_data, self.augmentation_factor
            )
        
        # Convert to tensor format
        tensor_data = []
        for sample in processed_raw_data:
            tensor_sample = self._convert_to_tensors(sample)
            tensor_data.append(tensor_sample)
        
        # Cache processed data
        if self.cache_processed and hasattr(self, 'cache_path'):
            self.logger.info(f"Caching processed data to {self.cache_path}")
            torch.save(tensor_data, self.cache_path)
        
        return tensor_data
    
    def _load_raw_data(self) -> List[Dict[str, Any]]:
        """Load raw data from various file formats"""
        raw_data = []
        
        if self.data_path.is_file():
            # Single file
            raw_data = self._load_single_file(self.data_path)
        elif self.data_path.is_dir():
            # Directory with multiple files
            for file_path in self.data_path.glob('*'):
                if file_path.suffix in ['.json', '.jsonl', '.csv']:
                    file_data = self._load_single_file(file_path)
                    raw_data.extend(file_data)
        else:
            # Generate synthetic data for testing
            self.logger.warning(f"Data path {self.data_path} not found, generating synthetic data")
            raw_data = self._generate_synthetic_data()
        
        self.logger.info(f"Loaded {len(raw_data)} raw samples")
        return raw_data
    
    def _load_single_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Load data from a single file"""
        data = []
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = [data]
            
            elif file_path.suffix == '.jsonl':
                with open(file_path, 'r') as f:
                    data = [json.loads(line) for line in f]
            
            elif file_path.suffix == '.csv':
                df = pd.read_csv(file_path)
                data = df.to_dict('records')
            
        except Exception as e:
            self.logger.error(f"Error loading {file_path}: {e}")
            data = []
        
        return data
    
    def _generate_synthetic_data(self, num_samples: int = 1000) -> List[Dict[str, Any]]:
        """Generate synthetic compatibility data for testing"""
        synthetic_data = []
        
        # Dimension names
        dimensions = ['love', 'friendship', 'communication', 'emotional',
                     'intellectual', 'physical', 'spiritual', 'career',
                     'family', 'trust', 'values', 'overall']
        
        for _ in range(num_samples):
            sign1 = random.randint(0, 11)
            sign2 = random.randint(0, 11)
            
            # Generate realistic compatibility scores based on traditional astrology
            base_compatibility = self._calculate_synthetic_compatibility(sign1, sign2)
            
            # Add some noise
            scores = {}
            for dim in dimensions:
                noise = random.uniform(-0.1, 0.1)
                score = np.clip(base_compatibility + noise, 0.0, 1.0)
                scores[dim] = score
            
            sample = {
                'sign1': sign1,
                'sign2': sign2,
                'birth_data1': {
                    'hour': random.randint(0, 23),
                    'day': random.randint(1, 28),
                    'month': random.randint(1, 12),
                    'latitude': random.uniform(-60, 60),
                    'longitude': random.uniform(-180, 180)
                },
                'birth_data2': {
                    'hour': random.randint(0, 23),
                    'day': random.randint(1, 28),
                    'month': random.randint(1, 12),
                    'latitude': random.uniform(-60, 60),
                    'longitude': random.uniform(-180, 180)
                },
                'context': {
                    'relationship_type': random.choice(['romantic', 'friendship', 'business']),
                    'duration_months': random.randint(0, 120),
                    'age_difference': random.randint(0, 20)
                },
                'compatibility_scores': scores
            }
            
            synthetic_data.append(sample)
        
        return synthetic_data
    
    def _calculate_synthetic_compatibility(self, sign1: int, sign2: int) -> float:
        """Calculate synthetic compatibility score based on simple astrological rules"""
        # Element compatibility
        elements = ['fire', 'earth', 'air', 'water']
        sign_elements = [elements[i % 4] for i in [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]]
        
        elem1 = sign_elements[sign1]
        elem2 = sign_elements[sign2]
        
        # Base compatibility by element
        if elem1 == elem2:
            base_score = 0.7  # Same element
        elif (elem1, elem2) in [('fire', 'air'), ('air', 'fire'), ('earth', 'water'), ('water', 'earth')]:
            base_score = 0.8  # Complementary elements
        else:
            base_score = 0.5  # Neutral or challenging
        
        # Adjust for angular relationship
        angle_diff = abs(sign1 - sign2) * 30
        angle_diff = min(angle_diff, 360 - angle_diff)
        
        if 55 <= angle_diff <= 65 or 115 <= angle_diff <= 125:  # Harmonious aspects
            base_score += 0.1
        elif 85 <= angle_diff <= 95 or 175 <= angle_diff <= 185:  # Challenging aspects
            base_score -= 0.1
        
        return np.clip(base_score, 0.0, 1.0)
    
    def _convert_to_tensors(self, sample: Dict[str, Any]) -> Dict[str, torch.Tensor]:
        """Convert processed sample to tensors"""
        tensor_sample = {}
        
        # Convert numpy arrays to tensors
        for key, value in sample.items():
            if isinstance(value, np.ndarray):
                tensor_sample[key] = torch.from_numpy(value.copy()).float()
            elif isinstance(value, (int, float)):
                tensor_sample[key] = torch.tensor(value, dtype=torch.float32)
            elif isinstance(value, list):
                tensor_sample[key] = torch.tensor(value, dtype=torch.float32)
            else:
                tensor_sample[key] = value
        
        # Ensure required tensors exist
        required_keys = ['sign1_idx', 'sign2_idx', 'aspect_matrix', 'context_features', 'targets']
        for key in required_keys:
            if key not in tensor_sample:
                if key in ['sign1_idx', 'sign2_idx']:
                    tensor_sample[key] = torch.tensor(0, dtype=torch.long)
                elif key == 'aspect_matrix':
                    tensor_sample[key] = torch.zeros(12, 12, dtype=torch.float32)
                elif key == 'context_features':
                    tensor_sample[key] = torch.zeros(50, dtype=torch.float32)
                elif key == 'targets':
                    tensor_sample[key] = torch.zeros(12, dtype=torch.float32)
        
        # Ensure correct dtypes
        tensor_sample['sign1_idx'] = tensor_sample['sign1_idx'].long()
        tensor_sample['sign2_idx'] = tensor_sample['sign2_idx'].long()
        
        return tensor_sample
    
    def __len__(self) -> int:
        return len(self.data)
    
    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        """Get a single sample"""
        sample = self.data[idx].copy()
        
        # Apply augmentation pipeline if enabled and this is training
        if self.augment and self.split == 'train' and self.augmentation_pipeline:
            # Convert tensors back to numpy for augmentation
            numpy_sample = {}
            for key, value in sample.items():
                if torch.is_tensor(value):
                    numpy_sample[key] = value.numpy()
                else:
                    numpy_sample[key] = value
            
            # Apply augmentation
            augmented_sample = self.augmentation_pipeline(numpy_sample)
            
            # Convert back to tensors
            sample = self._convert_to_tensors(augmented_sample)
        
        return sample
    
    def get_sample_by_signs(self, sign1: int, sign2: int) -> Optional[Dict[str, torch.Tensor]]:
        """Get a sample for specific sign combination"""
        for sample in self.data:
            if (sample['sign1_idx'].item() == sign1 and 
                sample['sign2_idx'].item() == sign2):
                return sample
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get dataset statistics"""
        if not self.data:
            return {}
        
        # Sign distribution
        sign1_counts = {}
        sign2_counts = {}
        target_stats = {'mean': [], 'std': []}
        
        for sample in self.data:
            s1 = sample['sign1_idx'].item()
            s2 = sample['sign2_idx'].item()
            
            sign1_counts[s1] = sign1_counts.get(s1, 0) + 1
            sign2_counts[s2] = sign2_counts.get(s2, 0) + 1
            
            targets = sample['targets'].numpy()
            target_stats['mean'].append(np.mean(targets))
            target_stats['std'].append(np.std(targets))
        
        stats = {
            'dataset_size': len(self.data),
            'sign1_distribution': sign1_counts,
            'sign2_distribution': sign2_counts,
            'target_mean': np.mean(target_stats['mean']),
            'target_std': np.mean(target_stats['std']),
            'feature_shapes': {
                key: sample[key].shape for key, sample in 
                [(k, self.data[0]) for k in self.data[0].keys() if torch.is_tensor(self.data[0][k])]
            }
        }
        
        return stats
    
    def split_by_signs(self, train_ratio: float = 0.7, 
                      val_ratio: float = 0.15) -> Tuple['CompatibilityDataset', 'CompatibilityDataset', 'CompatibilityDataset']:
        """Split dataset by sign combinations to avoid data leakage"""
        # Get unique sign combinations
        sign_combinations = set()
        for sample in self.data:
            s1 = sample['sign1_idx'].item()
            s2 = sample['sign2_idx'].item()
            sign_combinations.add((min(s1, s2), max(s1, s2)))
        
        # Split combinations
        combinations_list = list(sign_combinations)
        random.shuffle(combinations_list)
        
        train_size = int(len(combinations_list) * train_ratio)
        val_size = int(len(combinations_list) * val_ratio)
        
        train_combinations = set(combinations_list[:train_size])
        val_combinations = set(combinations_list[train_size:train_size + val_size])
        test_combinations = set(combinations_list[train_size + val_size:])
        
        # Split samples
        train_samples = []
        val_samples = []
        test_samples = []
        
        for sample in self.data:
            s1 = sample['sign1_idx'].item()
            s2 = sample['sign2_idx'].item()
            combo = (min(s1, s2), max(s1, s2))
            
            if combo in train_combinations:
                train_samples.append(sample)
            elif combo in val_combinations:
                val_samples.append(sample)
            else:
                test_samples.append(sample)
        
        # Create new datasets
        train_dataset = CompatibilityDataset.__new__(CompatibilityDataset)
        train_dataset.data = train_samples
        train_dataset.split = 'train'
        train_dataset.preprocessor = self.preprocessor
        
        val_dataset = CompatibilityDataset.__new__(CompatibilityDataset)
        val_dataset.data = val_samples
        val_dataset.split = 'val'
        val_dataset.preprocessor = self.preprocessor
        
        test_dataset = CompatibilityDataset.__new__(CompatibilityDataset)
        test_dataset.data = test_samples
        test_dataset.split = 'test'
        test_dataset.preprocessor = self.preprocessor
        
        return train_dataset, val_dataset, test_dataset
    
    def save_preprocessor(self, filepath: str):
        """Save the fitted preprocessor"""
        if self.preprocessor.is_fitted:
            self.preprocessor.save(filepath)
            self.logger.info(f"Preprocessor saved to {filepath}")
        else:
            self.logger.warning("Preprocessor not fitted, cannot save")


def create_compatibility_dataloaders(data_dir: str, 
                                    batch_size: int = 32,
                                    num_workers: int = 4,
                                    augment_train: bool = True,
                                    cache_processed: bool = True) -> Tuple[DataLoader, DataLoader, DataLoader]:
    """
    Create train, validation, and test data loaders
    
    Args:
        data_dir: Directory containing data files
        batch_size: Batch size for data loaders
        num_workers: Number of worker processes
        augment_train: Whether to augment training data
        cache_processed: Whether to cache processed data
        
    Returns:
        Tuple of (train_loader, val_loader, test_loader)
    """
    
    # Create full dataset
    full_dataset = CompatibilityDataset(
        data_path=data_dir,
        augment=augment_train,
        split='full',
        cache_processed=cache_processed
    )
    
    # Split dataset
    train_dataset, val_dataset, test_dataset = full_dataset.split_by_signs()
    
    # Create data loaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=torch.cuda.is_available(),
        drop_last=True
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=torch.cuda.is_available()
    )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=torch.cuda.is_available()
    )
    
    return train_loader, val_loader, test_loader


if __name__ == "__main__":
    # Test dataset creation
    import tempfile
    
    # Create temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        # Test dataset creation with synthetic data
        dataset = CompatibilityDataset(
            data_path=temp_dir,  # Empty directory will trigger synthetic data
            augment=True,
            augmentation_factor=2,
            split='train'
        )
        
        print(f"Dataset size: {len(dataset)}")
        
        # Test getting a sample
        sample = dataset[0]
        print(f"Sample keys: {list(sample.keys())}")
        print(f"Sample shapes: {[(k, v.shape) for k, v in sample.items() if torch.is_tensor(v)]}")
        
        # Test statistics
        stats = dataset.get_statistics()
        print(f"Dataset statistics: {stats}")
        
        # Test data loader
        loader = DataLoader(dataset, batch_size=4, shuffle=True)
        batch = next(iter(loader))
        print(f"Batch keys: {list(batch.keys())}")
        print(f"Batch shapes: {[(k, v.shape) for k, v in batch.items() if torch.is_tensor(v)]}")
        
        # Test dataset splitting
        train_ds, val_ds, test_ds = dataset.split_by_signs()
        print(f"Split sizes: Train={len(train_ds)}, Val={len(val_ds)}, Test={len(test_ds)}")
        
        # Test data loader creation
        train_loader, val_loader, test_loader = create_compatibility_dataloaders(
            temp_dir, batch_size=8, num_workers=0
        )
        print(f"Data loader sizes: Train={len(train_loader)}, Val={len(val_loader)}, Test={len(test_loader)}")
        
        print("Dataset testing completed successfully!")