namespace CRSchatbotAPI.DTO
{
    public class CollegeInputDto
    {
        public string Name { get; set; }
        public string Location { get; set; }
        public string Type { get; set; }
        public string ContactNumber { get; set; }
        public string Email { get; set; }
        public bool HostelAvailability { get; set; }

        public List<DepartmentInputDto>? Departments { get; set; } = new();
    }

}
