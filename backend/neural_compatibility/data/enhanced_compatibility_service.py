"""
Enhanced Compatibility Service
============================

Advanced compatibility analysis service that integrates:
1. Discovered 144 combinations data pack as foundation
2. Neural AI enhancement layer
3. User context personalization
4. 12-dimensional analysis framework
5. Premium tier feature gating
"""

import json
import pandas as pd
import numpy as np
import torch
import torch.nn.functional as F
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import logging
from datetime import datetime, timedelta
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time

# Import existing neural components
from .compatibility_dataset import CompatibilityDataset
from ..models.compatibility_network import CompatibilityNeuralNetwork, ModelFactory
from ..models.embeddings import CompatibilityEmbeddings


@dataclass
class CompatibilityDimensions:
    """Enhanced 12-dimensional compatibility framework"""
    # Core 6 dimensions (from discovered pack)
    overall: float
    chemistry: float
    emotional: float
    communication: float
    values: float
    stability: float

    # New AI-enhanced dimensions
    spiritual: float
    lifestyle: float
    growth: float
    family: float
    adventure: float
    conflict_resolution: float

    def to_dict(self) -> Dict[str, float]:
        return asdict(self)

    @classmethod
    def from_base_scores(cls, base_scores: Dict[str, int], neural_enhancements: Dict[str, float]):
        """Create from discovered pack base scores + neural enhancements"""
        # Convert base scores to 0-1 range
        normalized_base = {k: v / 99.0 for k, v in base_scores.items()}

        return cls(
            overall=normalized_base.get('overall', 0.5),
            chemistry=normalized_base.get('chemistry', 0.5),
            emotional=normalized_base.get('emotional', 0.5),
            communication=normalized_base.get('communication', 0.5),
            values=normalized_base.get('values', 0.5),
            stability=normalized_base.get('stability', 0.5),

            # AI-enhanced dimensions
            spiritual=neural_enhancements.get('spiritual', 0.5),
            lifestyle=neural_enhancements.get('lifestyle', 0.5),
            growth=neural_enhancements.get('growth', 0.5),
            family=neural_enhancements.get('family', 0.5),
            adventure=neural_enhancements.get('adventure', 0.5),
            conflict_resolution=neural_enhancements.get('conflict_resolution', 0.5),
        )


@dataclass
class UserContext:
    """User context for personalized analysis"""
    age: Optional[int] = None
    relationship_experience: int = 0  # Number of previous relationships
    communication_style: str = 'balanced'  # direct, diplomatic, intuitive, analytical
    conflict_style: str = 'collaborative'  # avoidant, competitive, accommodating, collaborative
    lifestyle_energy: int = 5  # 1-10 scale
    career_focus: str = 'balanced'  # career_driven, family_focused, balanced
    adventure_level: int = 5  # 1-10 scale
    spiritual_openness: int = 5  # 1-10 scale

    def to_vector(self) -> np.ndarray:
        """Convert to 50-dimensional vector for neural processing"""
        vector = np.zeros(50)

        # Age encoding (normalized to 0-1)
        if self.age:
            vector[0] = min(self.age / 100.0, 1.0)

        # Experience encoding
        vector[1] = min(self.relationship_experience / 10.0, 1.0)

        # Communication style one-hot encoding
        comm_styles = ['direct', 'diplomatic', 'intuitive', 'analytical']
        if self.communication_style in comm_styles:
            idx = comm_styles.index(self.communication_style)
            vector[2 + idx] = 1.0

        # Conflict style one-hot encoding
        conflict_styles = ['avoidant', 'competitive', 'accommodating', 'collaborative']
        if self.conflict_style in conflict_styles:
            idx = conflict_styles.index(self.conflict_style)
            vector[6 + idx] = 1.0

        # Lifestyle factors (normalized)
        vector[10] = self.lifestyle_energy / 10.0
        vector[11] = self.adventure_level / 10.0
        vector[12] = self.spiritual_openness / 10.0

        # Career focus encoding
        career_types = ['career_driven', 'family_focused', 'balanced']
        if self.career_focus in career_types:
            idx = career_types.index(self.career_focus)
            vector[13 + idx] = 1.0

        # Remaining positions for future extensions
        return vector


@dataclass
class RelationshipPhase:
    """Predicted relationship phase information"""
    name: str
    start_months: int
    duration_months: int
    intensity: float
    key_characteristics: List[str]
    success_factors: List[str]
    potential_challenges: List[str]
    recommended_activities: List[str]


@dataclass
class EnhancedCompatibilityResult:
    """Complete enhanced compatibility analysis result"""
    pair_id: str
    sign1: str
    sign2: str
    aspect: str
    compatibility_level: str  # A, M, R

    # 12-dimensional scores
    dimensions: CompatibilityDimensions

    # Rich content from base data
    base_summary: str
    strengths: List[str]
    challenges: List[str]
    tips: List[str]
    date_ideas: List[str]

    # AI-enhanced content
    personalized_insights: List[str]
    growth_opportunities: List[str]
    conflict_strategies: List[str]

    # Premium features
    relationship_timeline: Optional[List[RelationshipPhase]] = None
    compatibility_evolution: Optional[Dict[str, List[float]]] = None

    # Metadata
    analysis_confidence: float = 0.0
    processing_time_ms: int = 0
    model_version: str = "v2.0"
    premium_tier: str = "free"
    generated_at: datetime = None

    def __post_init__(self):
        if self.generated_at is None:
            self.generated_at = datetime.now()


class EnhancedCompatibilityService:
    """
    Advanced compatibility analysis service

    Features:
    - Integrates discovered 144 combinations pack
    - Neural AI enhancement layer
    - User context personalization
    - 12-dimensional analysis
    - Premium feature tiering
    - Performance optimization
    """

    def __init__(self, base_data_path: str, model_path: Optional[str] = None):
        self.logger = logging.getLogger(__name__)

        # Load discovered compatibility data pack
        self.base_data = self._load_base_compatibility_data(base_data_path)
        self.logger.info(f"Loaded {len(self.base_data)} base compatibility combinations")

        # Initialize neural model
        self.neural_model = self._initialize_neural_model(model_path)

        # Aspect weights for AI enhancement
        self.aspect_weights = {
            'conjunción': 1.0,      # Same sign - intense connection
            'sextil': 0.85,         # 60° - harmonious energy
            'trígono': 0.95,        # 120° - natural flow
            'cuadratura': 0.45,     # 90° - tension/growth
            'oposición': 0.65,      # 180° - attraction/conflict
            'inconjunción': 0.35    # 150° - adjustment needed
        }

        # Premium tier configurations
        self.tier_configs = {
            'free': {
                'dimensions': ['overall', 'chemistry', 'communication'],
                'max_insights': 3,
                'include_timeline': False,
                'include_ai_enhancement': False
            },
            'basic': {
                'dimensions': ['overall', 'chemistry', 'emotional', 'communication', 'values', 'stability'],
                'max_insights': 8,
                'include_timeline': False,
                'include_ai_enhancement': True
            },
            'pro': {
                'dimensions': 'all',
                'max_insights': 15,
                'include_timeline': True,
                'include_ai_enhancement': True
            },
            'elite': {
                'dimensions': 'all',
                'max_insights': 'unlimited',
                'include_timeline': True,
                'include_ai_enhancement': True,
                'include_continuous_learning': True
            }
        }

        # Thread pool for parallel processing
        self.executor = ThreadPoolExecutor(max_workers=4)

    def _load_base_compatibility_data(self, data_path: str) -> Dict[str, Dict]:
        """Load the discovered 144 combinations compatibility data"""
        base_data = {}

        try:
            # Load JSON data
            json_path = Path(data_path) / 'compatibilidad_zodiacal.json'
            with open(json_path, 'r', encoding='utf-8') as f:
                data_list = json.load(f)

            # Convert to lookup dictionary
            for item in data_list:
                pair_id = item['pair_id']
                base_data[pair_id] = item

            self.logger.info(f"Successfully loaded {len(base_data)} base compatibility combinations")

        except Exception as e:
            self.logger.error(f"Failed to load base compatibility data: {e}")
            # Fallback to empty data - service will use neural model only
            base_data = {}

        return base_data

    def _initialize_neural_model(self, model_path: Optional[str]) -> CompatibilityNeuralNetwork:
        """Initialize the neural compatibility model"""
        try:
            if model_path and Path(model_path).exists():
                # Load pre-trained model
                model = ModelFactory.create_standard_model()
                model.load_state_dict(torch.load(model_path, map_location='cpu'))
                self.logger.info(f"Loaded pre-trained model from {model_path}")
            else:
                # Use new model (will need training)
                model = ModelFactory.create_standard_model()
                self.logger.info("Initialized new neural model")

            model.eval()
            return model

        except Exception as e:
            self.logger.error(f"Failed to initialize neural model: {e}")
            # Return basic model as fallback
            return ModelFactory.create_lightweight_model()

    async def analyze_compatibility(
        self,
        sign1: str,
        sign2: str,
        premium_tier: str = 'free',
        user1_context: Optional[UserContext] = None,
        user2_context: Optional[UserContext] = None,
        include_timeline: bool = False
    ) -> EnhancedCompatibilityResult:
        """
        Perform enhanced compatibility analysis

        Args:
            sign1: First zodiac sign
            sign2: Second zodiac sign
            premium_tier: User's premium tier (free, basic, pro, elite)
            user1_context: First user's context for personalization
            user2_context: Second user's context for personalization
            include_timeline: Whether to generate relationship timeline

        Returns:
            Enhanced compatibility analysis result
        """
        start_time = time.perf_counter()

        # Normalize sign names
        sign1 = sign1.lower().strip()
        sign2 = sign2.lower().strip()
        pair_id = f"{sign1}_{sign2}"

        # Get base compatibility data
        base_data = self._get_base_compatibility(pair_id, sign1, sign2)

        # Apply neural AI enhancement
        neural_enhancements = await self._apply_neural_enhancement(
            base_data, user1_context, user2_context, premium_tier
        )

        # Create 12-dimensional scores
        dimensions = CompatibilityDimensions.from_base_scores(
            base_data['scores'],
            neural_enhancements
        )

        # Generate personalized insights
        personalized_insights = await self._generate_personalized_insights(
            base_data, dimensions, user1_context, user2_context, premium_tier
        )

        # Generate growth opportunities and conflict strategies
        growth_opportunities = self._generate_growth_opportunities(
            dimensions, user1_context, user2_context
        )
        conflict_strategies = self._generate_conflict_strategies(
            dimensions, base_data, user1_context, user2_context
        )

        # Generate relationship timeline (premium feature)
        timeline = None
        if include_timeline and self.tier_configs[premium_tier]['include_timeline']:
            timeline = await self._generate_relationship_timeline(
                dimensions, base_data, user1_context, user2_context
            )

        # Calculate processing time
        processing_time = int((time.perf_counter() - start_time) * 1000)

        # Create result
        result = EnhancedCompatibilityResult(
            pair_id=pair_id,
            sign1=sign1,
            sign2=sign2,
            aspect=base_data['aspect'],
            compatibility_level=base_data['level'],
            dimensions=dimensions,
            base_summary=base_data['summary'],
            strengths=base_data['strengths'],
            challenges=base_data['challenges'],
            tips=base_data['tips'],
            date_ideas=base_data['date_ideas'],
            personalized_insights=personalized_insights,
            growth_opportunities=growth_opportunities,
            conflict_strategies=conflict_strategies,
            relationship_timeline=timeline,
            analysis_confidence=self._calculate_confidence(dimensions, neural_enhancements),
            processing_time_ms=processing_time,
            premium_tier=premium_tier
        )

        self.logger.info(f"Compatibility analysis completed for {pair_id} in {processing_time}ms")
        return result

    def _get_base_compatibility(self, pair_id: str, sign1: str, sign2: str) -> Dict:
        """Get base compatibility data from discovered pack"""
        # Try exact match first
        if pair_id in self.base_data:
            base = self.base_data[pair_id]
        else:
            # Try reversed pair
            reversed_pair_id = f"{sign2}_{sign1}"
            if reversed_pair_id in self.base_data:
                base = self.base_data[reversed_pair_id]
            else:
                # Fallback: generate synthetic base data
                base = self._generate_synthetic_base_data(sign1, sign2)

        # Normalize scores to expected format
        return {
            'aspect': base.get('aspect', 'neutral'),
            'level': base.get('level', 'M'),
            'scores': {
                'overall': base.get('overall', 60),
                'chemistry': base.get('chemistry', 60),
                'emotional': base.get('emotional', 60),
                'communication': base.get('communication', 60),
                'values': base.get('values', 60),
                'stability': base.get('stability', 60),
            },
            'summary': base.get('summary', f"Compatibility analysis for {sign1} and {sign2}"),
            'strengths': base.get('strengths', ["Natural connection"]),
            'challenges': base.get('challenges', ["Different approaches"]),
            'tips': base.get('tips', ["Focus on communication"]),
            'date_ideas': base.get('date_ideas', ["Shared activities"]),
        }

    def _generate_synthetic_base_data(self, sign1: str, sign2: str) -> Dict:
        """Generate synthetic base data when discovered pack data is missing"""
        self.logger.warning(f"No base data found for {sign1}-{sign2}, generating synthetic data")

        # Simple element-based compatibility
        elements = {
            'aries': 'fire', 'leo': 'fire', 'sagittarius': 'fire',
            'taurus': 'earth', 'virgo': 'earth', 'capricorn': 'earth',
            'gemini': 'air', 'libra': 'air', 'aquarius': 'air',
            'cancer': 'water', 'scorpio': 'water', 'pisces': 'water'
        }

        elem1 = elements.get(sign1, 'unknown')
        elem2 = elements.get(sign2, 'unknown')

        # Base compatibility by element
        if elem1 == elem2:
            base_score = 70  # Same element
            level = 'M'
        elif (elem1, elem2) in [('fire', 'air'), ('air', 'fire'), ('earth', 'water'), ('water', 'earth')]:
            base_score = 75  # Complementary
            level = 'A'
        else:
            base_score = 55  # Challenging
            level = 'R'

        return {
            'aspect': 'synthetic',
            'level': level,
            'overall': base_score,
            'chemistry': base_score + np.random.randint(-10, 10),
            'emotional': base_score + np.random.randint(-10, 10),
            'communication': base_score + np.random.randint(-10, 10),
            'values': base_score + np.random.randint(-10, 10),
            'stability': base_score + np.random.randint(-10, 10),
            'summary': f"Synthetic compatibility analysis for {sign1.title()} and {sign2.title()}",
            'strengths': ["Element-based natural affinity"],
            'challenges': ["Requires deeper understanding"],
            'tips': ["Focus on building trust"],
            'date_ideas': ["Explore shared interests"],
        }

    async def _apply_neural_enhancement(
        self,
        base_data: Dict,
        user1_context: Optional[UserContext],
        user2_context: Optional[UserContext],
        premium_tier: str
    ) -> Dict[str, float]:
        """Apply neural AI enhancement to base compatibility scores"""

        # Check if AI enhancement is available for this tier
        if not self.tier_configs[premium_tier]['include_ai_enhancement']:
            # Return neutral enhancements for free tier
            return {
                'spiritual': 0.5,
                'lifestyle': 0.5,
                'growth': 0.5,
                'family': 0.5,
                'adventure': 0.5,
                'conflict_resolution': 0.5,
            }

        try:
            # Prepare inputs for neural model
            sign1_idx = torch.tensor(0, dtype=torch.long)  # Would need proper sign mapping
            sign2_idx = torch.tensor(1, dtype=torch.long)

            # Create aspect matrix
            aspect_matrix = torch.zeros(1, 12, 12)
            aspect_weight = self.aspect_weights.get(base_data['aspect'], 0.5)
            aspect_matrix[0, 0, 1] = aspect_weight
            aspect_matrix[0, 1, 0] = aspect_weight

            # Create context features
            context_features = torch.zeros(1, 50)
            if user1_context and user2_context:
                # Combine user contexts
                ctx1_vector = user1_context.to_vector()
                ctx2_vector = user2_context.to_vector()

                # Take average and difference for relationship dynamics
                context_features[0, :25] = torch.from_numpy((ctx1_vector[:25] + ctx2_vector[:25]) / 2)
                context_features[0, 25:] = torch.from_numpy(np.abs(ctx1_vector[:25] - ctx2_vector[:25]))

            # Run neural inference
            with torch.no_grad():
                predictions = self.neural_model(sign1_idx, sign2_idx, aspect_matrix, context_features)
                predictions = predictions.squeeze().numpy()

            # Map to new dimensions (indices 6-11 for the new dimensions)
            enhancements = {
                'spiritual': float(predictions[6]) if len(predictions) > 6 else 0.5,
                'lifestyle': float(predictions[7]) if len(predictions) > 7 else 0.5,
                'growth': float(predictions[8]) if len(predictions) > 8 else 0.5,
                'family': float(predictions[9]) if len(predictions) > 9 else 0.5,
                'adventure': float(predictions[10]) if len(predictions) > 10 else 0.5,
                'conflict_resolution': float(predictions[11]) if len(predictions) > 11 else 0.5,
            }

            return enhancements

        except Exception as e:
            self.logger.error(f"Neural enhancement failed: {e}")
            # Return fallback enhancements
            return {
                'spiritual': 0.5 + np.random.uniform(-0.1, 0.1),
                'lifestyle': 0.5 + np.random.uniform(-0.1, 0.1),
                'growth': 0.5 + np.random.uniform(-0.1, 0.1),
                'family': 0.5 + np.random.uniform(-0.1, 0.1),
                'adventure': 0.5 + np.random.uniform(-0.1, 0.1),
                'conflict_resolution': 0.5 + np.random.uniform(-0.1, 0.1),
            }

    async def _generate_personalized_insights(
        self,
        base_data: Dict,
        dimensions: CompatibilityDimensions,
        user1_context: Optional[UserContext],
        user2_context: Optional[UserContext],
        premium_tier: str
    ) -> List[str]:
        """Generate personalized insights based on user context"""
        insights = []
        max_insights = self.tier_configs[premium_tier]['max_insights']

        # Base insights from discovered data summary
        if base_data['summary']:
            insights.append(f"Core dynamic: {base_data['summary']}")

        # Dimension-based insights
        dim_dict = dimensions.to_dict()
        top_dimensions = sorted(dim_dict.items(), key=lambda x: x[1], reverse=True)[:3]

        for dimension, score in top_dimensions:
            if len(insights) >= max_insights and max_insights != 'unlimited':
                break

            if score > 0.7:
                insights.append(f"Strong {dimension} compatibility ({score:.1%}) - a natural strength in your relationship.")

        # Context-based personalized insights
        if user1_context and user2_context and premium_tier in ['pro', 'elite']:
            # Communication style compatibility
            if user1_context.communication_style == user2_context.communication_style:
                insights.append("You share similar communication styles, which will help avoid misunderstandings.")
            elif user1_context.communication_style == 'direct' and user2_context.communication_style == 'diplomatic':
                insights.append("Balance direct honesty with diplomatic sensitivity for optimal communication.")

            # Adventure level compatibility
            adventure_diff = abs(user1_context.adventure_level - user2_context.adventure_level)
            if adventure_diff <= 2:
                insights.append("Your adventure preferences are well-aligned - explore new experiences together!")
            elif adventure_diff >= 6:
                insights.append("Different adventure preferences - find a middle ground that excites both of you.")

        # Premium AI insights
        if premium_tier == 'elite':
            insights.append("🤖 AI Insight: Your relationship benefits from complementary energy patterns that create natural balance.")

        return insights[:max_insights] if max_insights != 'unlimited' else insights

    def _generate_growth_opportunities(
        self,
        dimensions: CompatibilityDimensions,
        user1_context: Optional[UserContext],
        user2_context: Optional[UserContext]
    ) -> List[str]:
        """Generate relationship growth opportunities"""
        opportunities = []
        dim_dict = dimensions.to_dict()

        # Find dimensions with room for growth (score 0.3 - 0.7)
        growth_dimensions = {k: v for k, v in dim_dict.items() if 0.3 <= v <= 0.7}

        for dimension, score in growth_dimensions.items():
            if dimension == 'communication':
                opportunities.append("Practice active listening and expressing needs clearly")
            elif dimension == 'spiritual':
                opportunities.append("Explore shared spiritual practices or philosophical discussions")
            elif dimension == 'growth':
                opportunities.append("Support each other's personal development goals")
            elif dimension == 'conflict_resolution':
                opportunities.append("Develop healthy conflict resolution patterns together")
            elif dimension == 'family':
                opportunities.append("Discuss and align on family goals and values")
            elif dimension == 'adventure':
                opportunities.append("Plan new shared experiences and adventures")

        return opportunities[:5]  # Limit to top 5

    def _generate_conflict_strategies(
        self,
        dimensions: CompatibilityDimensions,
        base_data: Dict,
        user1_context: Optional[UserContext],
        user2_context: Optional[UserContext]
    ) -> List[str]:
        """Generate conflict resolution strategies"""
        strategies = []

        # Base strategies from discovered data
        if base_data['challenges']:
            for challenge in base_data['challenges'][:2]:
                strategies.append(f"Address: {challenge}")

        # Dimension-based strategies
        dim_dict = dimensions.to_dict()
        low_dimensions = {k: v for k, v in dim_dict.items() if v < 0.4}

        for dimension in low_dimensions:
            if dimension == 'communication':
                strategies.append("Set aside regular time for open, honest communication")
            elif dimension == 'values':
                strategies.append("Respect differences in values while finding common ground")
            elif dimension == 'conflict_resolution':
                strategies.append("Practice 'taking breaks' during heated discussions")

        # Context-based strategies
        if user1_context and user2_context:
            if user1_context.conflict_style != user2_context.conflict_style:
                strategies.append("Acknowledge and respect each other's different conflict styles")

        return strategies[:4]  # Limit to top 4

    async def _generate_relationship_timeline(
        self,
        dimensions: CompatibilityDimensions,
        base_data: Dict,
        user1_context: Optional[UserContext],
        user2_context: Optional[UserContext]
    ) -> List[RelationshipPhase]:
        """Generate predicted relationship timeline (premium feature)"""
        timeline = []

        # Honeymoon Phase
        honeymoon_duration = max(2, int(dimensions.chemistry * 12))  # 2-12 months based on chemistry
        timeline.append(RelationshipPhase(
            name="Honeymoon Phase",
            start_months=0,
            duration_months=honeymoon_duration,
            intensity=dimensions.chemistry,
            key_characteristics=["High romance", "Frequent communication", "Idealization"],
            success_factors=["Enjoy the connection", "Build emotional intimacy"],
            potential_challenges=["Overlooking red flags", "Unrealistic expectations"],
            recommended_activities=base_data['date_ideas'][:3]
        ))

        # Adjustment Phase
        adjustment_start = honeymoon_duration
        adjustment_duration = max(3, int((1 - dimensions.conflict_resolution) * 18))
        timeline.append(RelationshipPhase(
            name="Adjustment Phase",
            start_months=adjustment_start,
            duration_months=adjustment_duration,
            intensity=0.6,
            key_characteristics=["Reality check", "First conflicts", "Learning patterns"],
            success_factors=["Open communication", "Patience", "Compromise"],
            potential_challenges=["Disillusionment", "Power struggles"],
            recommended_activities=["Conflict resolution practice", "Couples activities"]
        ))

        # Deep Connection Phase
        if dimensions.emotional > 0.6 and dimensions.spiritual > 0.5:
            deep_start = adjustment_start + adjustment_duration
            timeline.append(RelationshipPhase(
                name="Deep Connection Phase",
                start_months=deep_start,
                duration_months=12,
                intensity=dimensions.emotional,
                key_characteristics=["Emotional intimacy", "Shared values", "Future planning"],
                success_factors=["Vulnerability", "Shared goals", "Trust building"],
                potential_challenges=["Fear of intimacy", "Different timelines"],
                recommended_activities=["Deep conversations", "Shared goals planning"]
            ))

        # Long-term Stability Phase
        if dimensions.stability > 0.6:
            stable_start = timeline[-1].start_months + timeline[-1].duration_months
            timeline.append(RelationshipPhase(
                name="Long-term Stability",
                start_months=stable_start,
                duration_months=60,  # 5 years+
                intensity=dimensions.stability,
                key_characteristics=["Established patterns", "Mutual support", "Growth together"],
                success_factors=["Continuous growth", "Maintained romance", "Shared vision"],
                potential_challenges=["Complacency", "Growing apart"],
                recommended_activities=["Regular relationship check-ins", "New shared experiences"]
            ))

        return timeline

    def _calculate_confidence(self, dimensions: CompatibilityDimensions, enhancements: Dict[str, float]) -> float:
        """Calculate confidence score for the analysis"""
        # Base confidence from dimension consistency
        dim_values = list(dimensions.to_dict().values())
        dim_variance = np.var(dim_values)
        base_confidence = max(0.3, 1.0 - dim_variance)

        # Enhancement confidence from neural model uncertainty
        enhancement_variance = np.var(list(enhancements.values()))
        enhancement_confidence = max(0.3, 1.0 - enhancement_variance)

        # Combined confidence
        overall_confidence = (base_confidence + enhancement_confidence) / 2
        return min(0.95, max(0.3, overall_confidence))  # Clamp between 30% and 95%

    async def analyze_batch_compatibility(
        self,
        sign_pairs: List[Tuple[str, str]],
        premium_tier: str = 'free'
    ) -> List[EnhancedCompatibilityResult]:
        """Analyze multiple compatibility pairs in parallel"""
        tasks = []
        for sign1, sign2 in sign_pairs:
            task = self.analyze_compatibility(sign1, sign2, premium_tier)
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions
        valid_results = [r for r in results if isinstance(r, EnhancedCompatibilityResult)]

        self.logger.info(f"Batch analysis completed: {len(valid_results)}/{len(sign_pairs)} successful")
        return valid_results

    def get_available_combinations(self) -> List[str]:
        """Get all available compatibility combinations"""
        return list(self.base_data.keys())

    def get_service_stats(self) -> Dict[str, Any]:
        """Get service statistics"""
        return {
            'base_combinations_loaded': len(self.base_data),
            'neural_model_loaded': self.neural_model is not None,
            'model_info': self.neural_model.get_model_info() if self.neural_model else None,
            'supported_tiers': list(self.tier_configs.keys()),
            'aspect_weights': self.aspect_weights
        }


# Usage example and testing
if __name__ == "__main__":
    import asyncio

    async def test_enhanced_service():
        # Initialize service
        base_data_path = "/Users/alejandrocaceres/Desktop/appstore - zodia/compatibilidad_zodiacal_pack"
        service = EnhancedCompatibilityService(base_data_path)

        # Test basic analysis
        result = await service.analyze_compatibility(
            "aries", "leo",
            premium_tier="pro",
            user1_context=UserContext(age=25, communication_style="direct"),
            user2_context=UserContext(age=27, communication_style="diplomatic"),
            include_timeline=True
        )

        print(f"Analysis Result for {result.pair_id}:")
        print(f"Overall Score: {result.dimensions.overall:.2%}")
        print(f"Processing Time: {result.processing_time_ms}ms")
        print(f"Insights: {len(result.personalized_insights)}")
        print(f"Timeline Phases: {len(result.relationship_timeline) if result.relationship_timeline else 0}")

        # Test batch analysis
        pairs = [("aries", "leo"), ("taurus", "virgo"), ("gemini", "libra")]
        batch_results = await service.analyze_batch_compatibility(pairs, "basic")
        print(f"\nBatch analysis completed: {len(batch_results)} results")

        # Service stats
        stats = service.get_service_stats()
        print(f"\nService Stats: {stats}")

    # Run test
    asyncio.run(test_enhanced_service())