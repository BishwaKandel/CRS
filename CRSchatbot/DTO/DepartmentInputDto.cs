
namespace CRSchatbotAPI.DTO
{
    public class DepartmentInputDto
    {
        public string Name { get; set; }
        public int CollegeId { get; set; }  // FK only

        public List<CourseInputDto>? Courses { get; set; } = new();
    }

}
