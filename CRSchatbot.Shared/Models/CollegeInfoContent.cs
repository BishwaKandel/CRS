namespace CRSchatbot.Shared.Models
{
    public enum ContentType
    {
        Text,
        Graph,
        Table,
        Chart
    }

    public class CollegeInfoContent
    {
        public int Id { get; set; }

        public string Name { get; set; }
        public string Title { get; set; }
        public string Description { get; set; }

        public string Body { get; set; } // Rich content (e.g., HTML or Markdown)

        public ContentType Type { get; set; } // Enum instead of string

        public DateTime CreatedAt { get; set; }

        public int CreatedById { get; set; }
        public User CreatedBy { get; set; }

        // Optional relationships to target a specific entity
        public int? CollegeId { get; set; }
        public College College { get; set; }

        public int? DepartmentId { get; set; }
        public Department Department { get; set; }

        public int? CourseId { get; set; }
        public Course Course { get; set; }
    }
}
