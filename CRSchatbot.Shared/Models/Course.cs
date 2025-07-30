namespace CRSchatbot.Shared.Models
{
    public class Course
    {
        public int CourseId { get; set; }
        public string Name { get; set; }

        public int DepartmentId { get; set; }
        public Department Department { get; set; }

        public double AverageCutoffRank { get; set; }
        public decimal Fee { get; set; }
        public int TotalSeats { get; set; }
        public double FacultyToStudentRatio { get; set; }
        public bool InternshipOpportunities { get; set; }
        public bool ScholarshipOffered { get; set; }
        public int DurationInYears { get; set; }
        public required string AdmissionProcess { get; set; }
        public double Rating { get; set; }
    }
}
