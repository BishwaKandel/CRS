import os
import sys
from typing import Dict, List, Any, Optional, Tuple
import logging

# Add the parent directory to sys.path to allow imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from intent_entity.chatbot_pipeline import ChatbotPipeline
from sql_builder import CollegeDataExtractor, DatabaseConfig, CollegeInfo
from recommendation_engine import StudentProfile, CollegeRecommendationSystem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatbotIntegrator:
    """
    Integrates the chatbot pipeline (intent+entity) with SQL builder and recommendation engine
    to provide end-to-end college recommendation functionality.
    """
    
    def __init__(self, pipeline_path: str = 'intent_entity', db_config: Optional[DatabaseConfig] = None):
        """
        Initialize the integrator with pipeline, SQL builder, and recommendation engine
        
        Args:
            pipeline_path: Path to the intent and entity recognition models
            db_config: Database configuration for SQL queries
        """
        # Initialize chatbot pipeline for intent and entity recognition
        self.pipeline = ChatbotPipeline(
            intent_model_dir=os.path.join(pipeline_path, 'intent'),
            ner_model_dir=os.path.join(pipeline_path, 'ner')
        )
        
        # Initialize database connection with default config if none provided
        if db_config is None:
            db_config = DatabaseConfig(
                host='localhost',
                database='CollegeInfoSystem',
                user='root',
                password='',
                port=3306
            )
        self.db_extractor = CollegeDataExtractor(db_config)
        
        # Initialize recommendation engine
        self.recommender = CollegeRecommendationSystem(self.db_extractor)
    
    def map_intent_to_sql(self, intent: str, entities: Dict[str, List[str]]) -> Tuple[str, List[Any]]:
        """
        Map detected intent and entities to appropriate SQL query
        
        Args:
            intent: The detected intent from the pipeline
            entities: Dictionary of entity types and their values
            
        Returns:
            Tuple of (SQL query string, parameter list)
        """
        # Base query - can be expanded for different intents
        base_query = """
        SELECT 
            c.CollegeId, c.Name AS CollegeName, c.Location, c.Type, 
            c.ContactNumber, c.Email, c.HostelAvailability, c.Latitude, c.Longitude,
            d.DepartmentId, d.Name AS DepartmentName,
            co.CourseId, co.Name AS CourseName, co.AverageCutoffRank, co.Fee, 
            co.TotalSeats, co.FacultyToStudentRatio, co.PassPercentage, 
            co.InternshipOpportunities, co.GereralScholarship, co.SemesterScholarship,
            co.TotalQuotas, co.DurationInYears, co.AdmissionProcess, co.Rating
        FROM College c
        LEFT JOIN Department d ON c.CollegeId = d.CollegeId
        LEFT JOIN Courses co ON d.DepartmentId = co.DepartmentId
        WHERE co.CourseId IS NOT NULL
        """
        
        conditions = []
        params = []
        
        # Process entity types and add appropriate WHERE conditions
        if 'COLLEGE' in entities:
            college_names = entities['COLLEGE']
            or_conditions = []
            for name in college_names:
                or_conditions.append("c.Name LIKE %s")
                params.append(f"%{name}%")
            if or_conditions:
                conditions.append(f"({' OR '.join(or_conditions)})")
        
        if 'LOCATION' in entities:
            locations = entities['LOCATION']
            or_conditions = []
            for location in locations:
                or_conditions.append("c.Location LIKE %s")
                params.append(f"%{location}%")
            if or_conditions:
                conditions.append(f"({' OR '.join(or_conditions)})")
        
        if 'COURSE' in entities or 'DEPARTMENT' in entities:
            course_dept_conditions = []
            
            if 'COURSE' in entities:
                for course in entities['COURSE']:
                    course_dept_conditions.append("co.Name LIKE %s")
                    params.append(f"%{course}%")
            
            if 'DEPARTMENT' in entities:
                for dept in entities['DEPARTMENT']:
                    course_dept_conditions.append("d.Name LIKE %s")
                    params.append(f"%{dept}%")
            
            if course_dept_conditions:
                conditions.append(f"({' OR '.join(course_dept_conditions)})")
        
        if 'TYPE' in entities:
            college_types = entities['TYPE']
            or_conditions = []
            for ctype in college_types:
                or_conditions.append("c.Type = %s")
                params.append(ctype)
            if or_conditions:
                conditions.append(f"({' OR '.join(or_conditions)})")
        
        if 'HOSTEL' in entities and len(entities['HOSTEL']) > 0:
            # Assuming HOSTEL entity is detected as "YES", "AVAILABLE", etc.
            conditions.append("c.HostelAvailability = TRUE")
        
        if 'MAX_FEE' in entities and len(entities['MAX_FEE']) > 0:
            try:
                max_fee = float(entities['MAX_FEE'][0])
                conditions.append("co.Fee <= %s")
                params.append(max_fee)
            except (ValueError, TypeError):
                logger.warning(f"Invalid MAX_FEE entity: {entities['MAX_FEE'][0]}")
        
        # Add WHERE conditions to base query if any
        if conditions:
            base_query += " AND " + " AND ".join(conditions)
        
        # Add ordering based on intent
        if intent == "find_affordable_college":
            base_query += " ORDER BY co.Fee ASC"
        elif intent == "find_top_rated_college":
            base_query += " ORDER BY co.Rating DESC"
        else:
            base_query += " ORDER BY c.Name, d.Name, co.Name"
        
        return base_query, params
    
    def build_student_profile(self, entities: Dict[str, List[str]]) -> StudentProfile:
        """
        Build a student profile from detected entities for recommendation
        
        Args:
            entities: Dictionary of entity types and their values
            
        Returns:
            StudentProfile object with extracted preferences
        """
        profile = StudentProfile()
        
        # Set location preferences
        if 'LOCATION' in entities:
            profile.preferred_locations = entities['LOCATION']
        
        # Set course preferences
        if 'COURSE' in entities:
            profile.preferred_courses = entities['COURSE']
        
        # Set college type preference
        if 'TYPE' in entities and len(entities['TYPE']) > 0:
            profile.preferred_college_type = entities['TYPE'][0]
        
        # Set budget constraint
        if 'MAX_FEE' in entities and len(entities['MAX_FEE']) > 0:
            try:
                profile.budget_max = float(entities['MAX_FEE'][0])
            except (ValueError, TypeError):
                pass
        
        # Set hostel requirement
        if 'HOSTEL' in entities and len(entities['HOSTEL']) > 0:
            profile.hostel_required = True
        
        # Set entrance rank if provided
        if 'RANK' in entities and len(entities['RANK']) > 0:
            try:
                profile.entrance_rank = int(entities['RANK'][0])
            except (ValueError, TypeError):
                pass
        
        return profile
    
    def process_query(self, user_query: str) -> Dict[str, Any]:
        """
        Process a user query through the entire pipeline and return recommendations
        
        Args:
            user_query: Natural language query from the user
            
        Returns:
            Dictionary with pipeline results, SQL results, and recommendations
        """
        # Step 1: Process through NLP pipeline
        pipeline_result = self.pipeline.process_message(user_query)
        
        # Check if pipeline processing was successful
        if pipeline_result['status'] != 'success':
            return pipeline_result
        
        intent = pipeline_result['predicted_intent']
        entities = pipeline_result['entities']
        confidence = pipeline_result['confidence']
        
        # Step 2: Map intent/entities to SQL query
        sql_query, params = self.map_intent_to_sql(intent, entities)
        
        try:
            # Step 3: Execute SQL query
            sql_results = self.db_extractor.get_colleges_by_filters(sql_query, params)
            
            # Step 4: Build student profile from entities
            student_profile = self.build_student_profile(entities)
            
            # Step 5: Determine comparison factors based on intent/entities
            comparison_factors = []
            
            # Add location as factor if mentioned in entities
            if 'LOCATION' in entities:
                comparison_factors.append('location')
            
            # Add fee as factor if mentioned in intent or entities
            if 'MAX_FEE' in entities or 'fee' in intent.lower() or 'affordable' in intent.lower():
                comparison_factors.append('fee')
            
            # Add pass_rate as default or if quality is mentioned
            if 'quality' in intent.lower() or 'top' in intent.lower() or 'best' in intent.lower():
                comparison_factors.append('pass_rate')
            
            # Ensure at least one factor is selected (default to all three)
            if not comparison_factors:
                comparison_factors = ['location', 'fee', 'pass_rate']
            
            # Step 6: Get recommendations based on comparison factors
            recommendations = self.recommender.compare_colleges(
                profile=student_profile,
                factors=comparison_factors,
                top_n=5
            )
            
            # Step 7: Return complete result
            return {
                **pipeline_result,  # Include original pipeline results
                'sql_query': sql_query,
                'sql_params': params,
                'sql_results_count': len(sql_results),
                'comparison_factors': comparison_factors,
                'recommendations': [rec.to_dict() for rec in recommendations],
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Error in recommendation process: {str(e)}")
            return {
                **pipeline_result,  # Include original pipeline results
                'error': str(e),
                'status': 'error',
                'response': f"Sorry, I encountered an error while processing your request: {str(e)}"
            }

# Example usage
def example():
    integrator = ChatbotIntegrator()
    result = integrator.process_query("Show me affordable engineering colleges in Lalitpur with hostel facility")
    
    print("\n🔍 Intent: ", result['predicted_intent'])
    print("💯 Confidence: ", result['confidence'])
    print("🏷️ Entities: ", result['entities'])
    print("\n🎓 Top recommendations:")
    
    for i, rec in enumerate(result['recommendations'][:3], 1):
        print(f"\n{i}. {rec['college_name']} - {rec['course_name']}")
        print(f"   Match: {rec['match_percentage']:.1f}% | Fee: {rec['fee']}")
        print(f"   Location: {rec['location']}")
        print(f"   Reasoning: {rec['reasoning']}")

if __name__ == "__main__":
    example()
