import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import math
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
import warnings
warnings.filterwarnings('ignore')

# Import from the data extractor file
from data_extractor import CollegeInfo, CollegeDataExtractor, DatabaseConfig

class Priority(Enum):
    """Priority levels for different criteria"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class StudentProfile:
    """Student profile for personalized recommendations"""
    entrance_rank: Optional[int] = None
    budget_max: Optional[float] = None
    preferred_locations: List[str] = None
    preferred_courses: List[str] = None
    preferred_college_type: Optional[str] = None  # PUBLIC/PRIVATE
    hostel_required: bool = False
    internship_priority: Priority = Priority.MEDIUM
    scholarship_priority: Priority = Priority.MEDIUM
    rating_priority: Priority = Priority.HIGH
    pass_percentage_priority: Priority = Priority.MEDIUM
    location_proximity: Optional[Tuple[float, float]] = None  # (lat, lng)
    max_distance_km: Optional[float] = None
    
    def __post_init__(self):
        if self.preferred_locations is None:
            self.preferred_locations = []
        if self.preferred_courses is None:
            self.preferred_courses = []

@dataclass
class RecommendationScore:
    """Detailed scoring for recommendations"""
    overall_score: float
    affordability_score: float
    quality_score: float
    accessibility_score: float
    location_score: float
    feature_score: float
    reasoning: str

@dataclass
class CollegeRecommendation:
    """College recommendation with detailed scoring"""
    college_info: CollegeInfo
    score: RecommendationScore
    rank: int
    match_percentage: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for easy display"""
        data = self.college_info.to_dict()
        data.update({
            'recommendation_rank': self.rank,
            'match_percentage': self.match_percentage,
            'overall_score': self.score.overall_score,
            'affordability_score': self.score.affordability_score,
            'quality_score': self.score.quality_score,
            'accessibility_score': self.score.accessibility_score,
            'location_score': self.score.location_score,
            'feature_score': self.score.feature_score,
            'reasoning': self.score.reasoning
        })
        return data

class CollegeRecommendationSystem:
    """Advanced College Recommendation System"""
    
    def __init__(self, extractor: CollegeDataExtractor):
        self.extractor = extractor
        self.colleges_data: List[CollegeInfo] = []
        self.df: pd.DataFrame = None
        self.scaler = MinMaxScaler()
        self.feature_matrix = None
        
    def load_data(self):
        """Load and prepare data for recommendations"""
        print("Loading college data...")
        self.colleges_data = self.extractor.get_all_colleges_info()
        
        # Convert to DataFrame for easier analysis
        data_list = [college.to_dict() for college in self.colleges_data]
        self.df = pd.DataFrame(data_list)
        
        # Handle missing values
        self.df = self._clean_data()
        
        print(f"Loaded {len(self.colleges_data)} college programs")
        
    def _clean_data(self) -> pd.DataFrame:
        """Clean and prepare data"""
        df = self.df.copy()
        
        # Fill missing numerical values
        numerical_columns = ['fee', 'rating', 'pass_percentage', 'average_cutoff_rank', 
                           'total_seats', 'faculty_to_student_ratio', 'general_scholarship']
        
        for col in numerical_columns:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].median())
        
        # Fill missing categorical values
        categorical_columns = ['college_type', 'admission_process']
        for col in categorical_columns:
            if col in df.columns:
                df[col] = df[col].fillna('Unknown')
        
        # Convert boolean columns
        boolean_columns = ['hostel_availability', 'internship_opportunities']
        for col in boolean_columns:
            if col in df.columns:
                df[col] = df[col].fillna(False)
        
        return df
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two coordinates using Haversine formula"""
        if pd.isna(lat1) or pd.isna(lon1) or pd.isna(lat2) or pd.isna(lon2):
            return float('inf')
            
        R = 6371  # Earth's radius in kilometers
        
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        distance = R * c
        
        return distance
    
    def _calculate_affordability_score(self, college_info: Dict, profile: StudentProfile) -> float:
        """Calculate affordability score (0-1, higher is better)"""
        fee = college_info.get('fee', 0)
        scholarship = college_info.get('general_scholarship', 0)
        
        # If no budget specified, use median fee as reference
        if profile.budget_max is None:
            budget_max = self.df['fee'].median() * 1.2
        else:
            budget_max = profile.budget_max
        
        # Effective cost after scholarship
        effective_fee = fee * (1 - scholarship / 100)
        
        if effective_fee <= budget_max:
            # Within budget - score based on how much money is saved
            if budget_max > 0:
                score = 1 - (effective_fee / budget_max) * 0.7  # Max score 1, min 0.3
            else:
                score = 1.0
        else:
            # Over budget - penalty
            overage = effective_fee - budget_max
            score = max(0, 1 - (overage / budget_max))
        
        return min(1.0, max(0.0, score))
    
    def _calculate_quality_score(self, college_info: Dict, profile: StudentProfile) -> float:
        """Calculate quality score based on rating and pass percentage"""
        rating = college_info.get('rating', 0)
        pass_percentage = college_info.get('pass_percentage', 0)
        internship = college_info.get('internship_opportunities', False)
        
        # Normalize rating (assuming max is 5)
        rating_score = rating / 5.0
        
        # Normalize pass percentage
        pass_score = pass_percentage / 100.0
        
        # Internship bonus
        internship_score = 1.0 if internship else 0.5
        
        # Weight based on student priorities
        rating_weight = profile.rating_priority.value / 4.0
        pass_weight = profile.pass_percentage_priority.value / 4.0
        internship_weight = profile.internship_priority.value / 4.0
        
        # Weighted average
        total_weight = rating_weight + pass_weight + internship_weight
        if total_weight > 0:
            quality_score = (rating_score * rating_weight + 
                           pass_score * pass_weight + 
                           internship_score * internship_weight) / total_weight
        else:
            quality_score = (rating_score + pass_score + internship_score) / 3
        
        return min(1.0, max(0.0, quality_score))
    
    def _calculate_accessibility_score(self, college_info: Dict, profile: StudentProfile) -> float:
        """Calculate accessibility score based on cutoff rank"""
        cutoff_rank = college_info.get('average_cutoff_rank', float('inf'))
        student_rank = profile.entrance_rank
        
        if student_rank is None or cutoff_rank == 0:
            return 0.5  # Neutral score if no rank info
        
        if student_rank <= cutoff_rank:
            # Student can get admission
            buffer = cutoff_rank - student_rank
            # Higher buffer gives higher score
            score = min(1.0, 0.7 + (buffer / cutoff_rank) * 0.3)
        else:
            # Student might not get admission
            gap = student_rank - cutoff_rank
            score = max(0.0, 0.5 - (gap / cutoff_rank) * 0.5)
        
        return score
    
    def _calculate_location_score(self, college_info: Dict, profile: StudentProfile) -> float:
        """Calculate location score based on preferences"""
        location = college_info.get('location', '')
        college_lat = college_info.get('latitude', 0)
        college_lng = college_info.get('longitude', 0)
        
        score = 0.5  # Default neutral score
        
        # Check preferred locations
        if profile.preferred_locations:
            for pref_location in profile.preferred_locations:
                if pref_location.upper() in location.upper():
                    score = max(score, 0.9)
                    break
        
        # Check distance if coordinates are provided
        if profile.location_proximity and profile.max_distance_km:
            student_lat, student_lng = profile.location_proximity
            distance = self._calculate_distance(student_lat, student_lng, college_lat, college_lng)
            
            if distance <= profile.max_distance_km:
                # Closer is better
                distance_score = 1 - (distance / profile.max_distance_km) * 0.5
                score = max(score, distance_score)
            else:
                # Penalty for being too far
                score = min(score, 0.3)
        
        return min(1.0, max(0.0, score))
    
    def _calculate_feature_score(self, college_info: Dict, profile: StudentProfile) -> float:
        """Calculate feature score based on student preferences"""
        score = 0.5  # Start with neutral
        # College type preference
        college_type = college_info.get('college_type', '')
        if profile.preferred_college_type and college_type == profile.preferred_college_type:
            score += 0.2
        # Course preference
        course_name = college_info.get('course_name', '')
        if profile.preferred_courses:
            for pref_course in profile.preferred_courses:
                if pref_course.upper() in course_name.upper():
                    score += 0.2
                    break
        # Hostel preference
        hostel = college_info.get('hostel_availability', False)
        if profile.hostel_required:
            score += 0.2 if hostel else -0.1
        return min(1.0, max(0.0, score))

    def get_field_result(self, field: str) -> List[Dict[str, Any]]:
        """Return direct results for an individual field across all colleges"""
        if self.df is None:
            self.load_data()
        if field not in self.df.columns:
            raise ValueError(f"Field '{field}' not found in college data.")
        results = self.df[['Name', field]].sort_values(by=field, ascending=False).to_dict(orient='records')
        return results

    def get_field_result(self, field: str) -> List[Dict[str, any]]:
        """Return direct results for an individual field across all colleges"""
        if self.df is None:
            self.load_data()
        if field not in self.df.columns:
            raise ValueError(f"Field '{field}' not found in college data.")
        results = self.df[['Name', field]].sort_values(by=field, ascending=False).to_dict(orient='records')
        return results

    def compare_colleges(self, profile: StudentProfile, factors: list, top_n: int = 5) -> List[CollegeRecommendation]:
        """Compare colleges based on selected factors (location, fee, pass_rate)"""
        if self.df is None:
            self.load_data()
        factor_weights = {f: 1.0/len(factors) for f in factors}  # Equal weights
        recommendations = []
        for idx, row in self.df.iterrows():
            college_info = row.to_dict()
            score_sum = 0.0
            reasoning_parts = []
            if 'location' in factors:
                location_score = self._calculate_location_score(college_info, profile)
                score_sum += location_score * factor_weights['location']
                reasoning_parts.append(f"Location: {location_score:.2f}")
            if 'fee' in factors:
                fee_score = 1 - (college_info.get('fee', 0) / (self.df['fee'].max() if self.df['fee'].max() > 0 else 1))
                score_sum += fee_score * factor_weights['fee']
                reasoning_parts.append(f"Fee: {fee_score:.2f}")
            if 'pass_rate' in factors:
                pass_rate_score = college_info.get('pass_percentage', 0) / 100.0
                score_sum += pass_rate_score * factor_weights['pass_rate']
                reasoning_parts.append(f"Pass Rate: {pass_rate_score:.2f}")
            score = RecommendationScore(
                overall_score=score_sum,
                affordability_score=fee_score if 'fee' in factors else 0.0,
                quality_score=pass_rate_score if 'pass_rate' in factors else 0.0,
                accessibility_score=0.0,
                location_score=location_score if 'location' in factors else 0.0,
                feature_score=0.0,
                reasoning=", ".join(reasoning_parts)
            )
            recommendations.append(CollegeRecommendation(
                college_info=college_info,
                score=score,
                rank=0,
                match_percentage=score_sum * 100
            ))
        recommendations.sort(key=lambda x: x.score.overall_score, reverse=True)
        for i, rec in enumerate(recommendations):
            rec.rank = i + 1
        return recommendations[:top_n]