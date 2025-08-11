import mysql.connector
from mysql.connector import Error
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
import logging
from contextlib import contextmanager
from dataclasses import dataclass
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class College:
    """Data class for College information"""
    college_id: int
    name: str
    location: str
    type: str
    contact_number: str
    email: str
    hostel_availability: bool
    latitude: float
    longitude: float

@dataclass
class Department:
    """Data class for Department information"""
    department_id: int
    name: str
    college_id: int

@dataclass
class Course:
    """Data class for Course information"""
    course_id: int
    name: str
    average_cutoff_rank: int
    fee: float
    total_seats: int
    faculty_to_student_ratio: float
    pass_percentage: int
    internship_opportunities: bool
    general_scholarship: int
    semester_scholarship: str
    total_quotas: int
    duration_in_years: int
    admission_process: str
    rating: float
    department_id: int

@dataclass
class CollegeInfo:
    """Combined college information"""
    college: College
    department: Department
    course: Course
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for easy processing"""
        return {
            'college_id': self.college.college_id,
            'college_name': self.college.name,
            'location': self.college.location,
            'college_type': self.college.type,
            'contact_number': self.college.contact_number,
            'email': self.college.email,
            'hostel_availability': self.college.hostel_availability,
            'latitude': self.college.latitude,
            'longitude': self.college.longitude,
            'department_id': self.department.department_id,
            'department_name': self.department.name,
            'course_id': self.course.course_id,
            'course_name': self.course.name,
            'average_cutoff_rank': self.course.average_cutoff_rank,
            'fee': self.course.fee,
            'total_seats': self.course.total_seats,
            'faculty_to_student_ratio': self.course.faculty_to_student_ratio,
            'pass_percentage': self.course.pass_percentage,
            'internship_opportunities': self.course.internship_opportunities,
            'general_scholarship': self.course.general_scholarship,
            'semester_scholarship': self.course.semester_scholarship,
            'total_quotas': self.course.total_quotas,
            'duration_in_years': self.course.duration_in_years,
            'admission_process': self.course.admission_process,
            'rating': self.course.rating
        }

class DatabaseConfig:
    """Database configuration class"""
    def __init__(self, host: str = 'localhost', database: str = 'CollegeInfoSystem',
                 user: str = 'root', password: str = '', port: int = 3306):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

class CollegeDataExtractor:
    """Main data extraction class for College Information System"""
    
    def __init__(self, db_config: DatabaseConfig):
        self.db_config = db_config
        self.connection = None
        
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        connection = None
        try:
            connection = mysql.connector.connect(
                host=self.db_config.host,
                database=self.db_config.database,
                user=self.db_config.user,
                password=self.db_config.password,
                port=self.db_config.port,
                autocommit=True
            )
            yield connection
        except Error as e:
            logger.error(f"Database connection error: {e}")
            raise
        finally:
            if connection and connection.is_connected():
                connection.close()
    
    def execute_query(self, query: str, params: List[Any] = None) -> List[Dict[str, Any]]:
        """Execute a query and return results as list of dictionaries"""
        try:
            with self.get_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, params or [])
                results = cursor.fetchall()
                cursor.close()
                
                logger.info(f"Query executed successfully. Retrieved {len(results)} records.")
                return results
                
        except Error as e:
            logger.error(f"Error executing query: {e}")
            logger.error(f"Query: {query}")
            logger.error(f"Params: {params}")
            raise
    
    def execute_query_to_dataframe(self, query: str, params: List[Any] = None) -> pd.DataFrame:
        """Execute query and return results as pandas DataFrame"""
        try:
            with self.get_connection() as connection:
                df = pd.read_sql(query, connection, params=params)
                logger.info(f"Query executed successfully. Retrieved {len(df)} records.")
                return df
                
        except Error as e:
            logger.error(f"Error executing query to DataFrame: {e}")
            raise
    
    def get_all_colleges_info(self) -> List[CollegeInfo]:
        """Get complete information for all colleges with their departments and courses"""
        query = """
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
        ORDER BY c.Name, d.Name, co.Name
        """
        
        results = self.execute_query(query)
        return self._convert_to_college_info_list(results)
    
    def get_colleges_by_filters(self, query: str, params: List[Any] = None) -> List[CollegeInfo]:
        """
        Get colleges based on custom query from query builder
        
        Args:
            query: SQL query string with placeholders
            params: List of parameters for the query placeholders
            
        Returns:
            List of CollegeInfo objects matching the query
        """
        results = self.execute_query(query, params)
        return self._convert_to_college_info_list(results)
    
    def get_colleges_dataframe(self, query: str, params: List[Any] = None) -> pd.DataFrame:
        """Get colleges as pandas DataFrame for analysis"""
        return self.execute_query_to_dataframe(query, params)
    
    def _convert_to_college_info_list(self, results: List[Dict[str, Any]]) -> List[CollegeInfo]:
        """Convert database results to CollegeInfo objects"""
        college_info_list = []
        
        for row in results:
            # Handle case where some fields might be None
            if row.get('CollegeId') is None:
                continue
                
            college = College(
                college_id=row['CollegeId'],
                name=row['CollegeName'],
                location=row['Location'],
                type=row['Type'],
                contact_number=row['ContactNumber'] or '',
                email=row['Email'] or '',
                hostel_availability=bool(row['HostelAvailability']),
                latitude=float(row['Latitude']) if row['Latitude'] else 0.0,
                longitude=float(row['Longitude']) if row['Longitude'] else 0.0
            )
            
            department = Department(
                department_id=row['DepartmentId'] or 0,
                name=row['DepartmentName'] or '',
                college_id=row['CollegeId']
            )
            
            course = Course(
                course_id=row.get('CourseId', 0) or 0,
                name=row.get('CourseName', '') or '',
                average_cutoff_rank=row.get('AverageCutoffRank', 0) or 0,
                fee=float(row.get('Fee', 0) or 0),
                total_seats=row.get('TotalSeats', 0) or 0,
                faculty_to_student_ratio=float(row.get('FacultyToStudentRatio', 0) or 0),
                pass_percentage=row.get('PassPercentage', 0) or 0,
                internship_opportunities=bool(row.get('InternshipOpportunities', False)),
                general_scholarship=row.get('GereralScholarship', 0) or 0,
                semester_scholarship=row.get('SemesterScholarship', '') or '',
                total_quotas=row.get('TotalQuotas', 0) or 0,
                duration_in_years=row.get('DurationInYears', 4) or 4,
                admission_process=row.get('AdmissionProcess', '') or '',
                rating=float(row.get('Rating', 0) or 0),
                department_id=row['DepartmentId'] or 0
            )
            
            college_info_list.append(CollegeInfo(college, department, course))
        
        return college_info_list
    
    # ==================== SPECIFIC DATA EXTRACTION METHODS ====================
    
    def get_course_statistics(self) -> pd.DataFrame:
        """Get statistical summary of courses"""
        query = """
        SELECT 
            co.Name AS course_name,
            COUNT(*) as total_colleges_offering,
            AVG(co.Fee) as average_fee,
            MIN(co.Fee) as min_fee,
            MAX(co.Fee) as max_fee,
            AVG(co.Rating) as average_rating,
            AVG(co.PassPercentage) as average_pass_percentage,
            AVG(co.AverageCutoffRank) as average_cutoff_rank,
            MIN(co.AverageCutoffRank) as best_cutoff_rank,
            MAX(co.AverageCutoffRank) as worst_cutoff_rank,
            SUM(co.TotalSeats) as total_seats_available,
            AVG(co.GereralScholarship) as average_scholarship
        FROM Courses co
        GROUP BY co.Name
        ORDER BY average_rating DESC, average_fee ASC
        """
        return self.execute_query_to_dataframe(query)
    
    def get_college_statistics(self) -> pd.DataFrame:
        """Get statistical summary of colleges"""
        query = """
        SELECT 
            c.Name as college_name,
            c.Location,
            c.Type as college_type,
            COUNT(DISTINCT d.DepartmentId) as total_departments,
            COUNT(co.CourseId) as total_courses,
            AVG(co.Fee) as average_fee,
            AVG(co.Rating) as average_rating,
            AVG(co.PassPercentage) as average_pass_percentage,
            SUM(co.TotalSeats) as total_seats,
            c.HostelAvailability as has_hostel
        FROM College c
        LEFT JOIN Department d ON c.CollegeId = d.CollegeId
        LEFT JOIN Courses co ON d.DepartmentId = co.DepartmentId
        WHERE co.CourseId IS NOT NULL
        GROUP BY c.CollegeId, c.Name, c.Location, c.Type, c.HostelAvailability
        ORDER BY average_rating DESC, average_fee ASC
        """
        return self.execute_query_to_dataframe(query)
    
    def get_location_statistics(self) -> pd.DataFrame:
        """Get statistics by location"""
        query = """
        SELECT 
            c.Location,
            COUNT(DISTINCT c.CollegeId) as total_colleges,
            COUNT(co.CourseId) as total_courses,
            AVG(co.Fee) as average_fee,
            AVG(co.Rating) as average_rating,
            SUM(co.TotalSeats) as total_seats
        FROM College c
        LEFT JOIN Department d ON c.CollegeId = d.CollegeId
        LEFT JOIN Courses co ON d.DepartmentId = co.DepartmentId
        WHERE co.CourseId IS NOT NULL
        GROUP BY c.Location
        ORDER BY total_colleges DESC, average_rating DESC
        """
        return self.execute_query_to_dataframe(query)
    
    def get_fee_distribution(self) -> pd.DataFrame:
        """Get fee distribution analysis"""
        query = """
        SELECT 
            co.Name as course_name,
            MIN(co.Fee) as min_fee,
            MAX(co.Fee) as max_fee,
            AVG(co.Fee) as avg_fee,
            STDDEV(co.Fee) as fee_std_dev,
            COUNT(*) as colleges_count
        FROM Courses co
        GROUP BY co.Name
        ORDER BY avg_fee DESC
        """
        return self.execute_query_to_dataframe(query)
    
    def get_top_colleges_by_rating(self, limit: int = 10) -> List[CollegeInfo]:
        """Get top colleges by rating"""
        query = """
        SELECT DISTINCT
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
        ORDER BY co.Rating DESC, co.PassPercentage DESC
        LIMIT %s
        """
        results = self.execute_query(query, [limit])
        return self._convert_to_college_info_list(results)
    
    def get_affordable_courses(self, max_fee: float, limit: int = 10) -> List[CollegeInfo]:
        """Get most affordable courses under given fee"""
        query = """
        SELECT DISTINCT
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
        WHERE co.CourseId IS NOT NULL AND co.Fee <= %s
        ORDER BY co.Fee ASC, co.Rating DESC
        LIMIT %s
        """
        results = self.execute_query(query, [max_fee, limit])
        return self._convert_to_college_info_list(results)
    
    def export_to_json(self, data: List[CollegeInfo], filename: str):
        """Export college info to JSON file"""
        try:
            data_dict = [item.to_dict() for item in data]
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data_dict, f, indent=2, default=str)
            logger.info(f"Data exported to {filename}")
        except Exception as e:
            logger.error(f"Error exporting to JSON: {e}")
            raise
    
    def export_to_csv(self, query: str, filename: str, params: List[Any] = None):
        """Export query results directly to CSV"""
        try:
            df = self.execute_query_to_dataframe(query, params)
            df.to_csv(filename, index=False)
            logger.info(f"Data exported to {filename}")
        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")
            raise

# ==================== USAGE EXAMPLES ====================

def example_usage():
    """Demonstrate data extraction usage"""
    
    # Database configuration
    db_config = DatabaseConfig(
        host='localhost',
        database='CollegeInfoSystem',
        user='root',
        password='your_password'  # Update with your password
    )
    
    # Initialize extractor
    extractor = CollegeDataExtractor(db_config)
    
    try:
        # Example 1: Get all colleges
        print("=== Getting all college information ===")
        all_colleges = extractor.get_all_colleges_info()
        print(f"Total records: {len(all_colleges)}")
        
        # Example 2: Get statistics
        print("\n=== Course Statistics ===")
        course_stats = extractor.get_course_statistics()
        print(course_stats.head())
        
        print("\n=== College Statistics ===")
        college_stats = extractor.get_college_statistics()
        print(college_stats.head())
        
        # Example 3: Get top colleges
        print("\n=== Top 5 Colleges by Rating ===")
        top_colleges = extractor.get_top_colleges_by_rating(5)
        for college_info in top_colleges:
            print(f"{college_info.college.name} - {college_info.course.name} - Rating: {college_info.course.rating}")
        
        # Example 4: Get affordable courses
        print("\n=== Affordable Courses (under 1M) ===")
        affordable = extractor.get_affordable_courses(1000000, 5)
        for college_info in affordable:
            print(f"{college_info.college.name} - {college_info.course.name} - Fee: {college_info.course.fee}")
        
        # Example 5: Export to JSON
        extractor.export_to_json(top_colleges, "top_colleges.json")
        
        # Example 6: Export statistics to CSV
        extractor.export_to_csv(
            "SELECT * FROM College c LEFT JOIN Department d ON c.CollegeId = d.CollegeId LEFT JOIN Courses co ON d.DepartmentId = co.DepartmentId", 
            "college_data.csv"
        )
        
    except Exception as e:
        logger.error(f"Error in example usage: {e}")

if __name__ == "__main__":
    example_usage()