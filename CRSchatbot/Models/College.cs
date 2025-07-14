namespace CRSchatbotAPI.Models
{
    public class College
    {
        public int CollegeId { get; set; }
        public string Name { get; set; }
        public string Location { get; set; }
        public string Type { get; set; } // e.g. Government, Private
        public string ContactNumber { get; set; }
        public string Email { get; set; }
        public bool HostelAvailability { get; set; }

        public required ICollection<Department> Departments { get; set; }
    }
}
