namespace CRSchatbotAPI.DTO
{
    public class CollegeInfoContentInputDto
    {
        public string Name { get; set; }
        public string Title { get; set; }
        public string Description { get; set; }
        public string Body { get; set; } // Rich content (e.g., HTML or Markdown)
        public string Type { get; set; } // Enum as string for simplicity
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
        public int CreatedById { get; set; } // User ID of the creator
        public int? CollegeId { get; set; } // Optional relationship to a specific college
        public int? DepartmentId { get; set; } // Optional relationship to a specific department
        public int? CourseId { get; set; } // Optional relationship to a specific course
    }
}
