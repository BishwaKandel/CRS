namespace CRSchatbotAPI.Models
{
    public class Department
    {
        public int DepartmentId { get; set; }
        public string Name { get; set; }

        public int CollegeId { get; set; }
        public College College { get; set; }

        public ICollection<Course> Courses { get; set; }
    }
}
