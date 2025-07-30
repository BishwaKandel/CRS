using CRSchatbotAPI.Data;
using CRSchatbotAPI.DTO;
using CRSchatbot.Shared.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace CRSchatbotAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class CourseController : Controller
    {
        private readonly AppDbContext _context;

        public CourseController(AppDbContext context)
        {
            _context = context;
        }

        // Create a new course for a department
        [HttpPost("/departments/{departmentId}/courses")]
        public async Task<IActionResult> AddCourseToDepartment(int departmentId, [FromBody] CourseInputDto dto)
        {
            var department = await _context.Departments.FindAsync(departmentId);
            if (department == null)
                return NotFound("Department not found");
            var course = new Course
            {
                Name = dto.Name,
                DepartmentId = departmentId,
                AverageCutoffRank = dto.AverageCutoffRank,
                Fee = dto.Fee,
                TotalSeats = dto.TotalSeats,
                FacultyToStudentRatio = dto.FacultyToStudentRatio,
                InternshipOpportunities = dto.InternshipOpportunities,
                ScholarshipOffered = dto.ScholarshipOffered,
                DurationInYears = dto.DurationInYears,
                AdmissionProcess = dto.AdmissionProcess,
                Rating = dto.Rating
            };
            _context.Courses.Add(course);
            await _context.SaveChangesAsync();
            return Ok(new { message = "Course added", courseId = course.CourseId });
        }


        // Get all courses by department ID
        [HttpGet("GetCoursesByDepartment/{departmentId}")]
        public async Task<IActionResult> GetCoursesByDepartment(int departmentId)
        {
            var courses = await _context.Courses
                .Where(c => c.DepartmentId == departmentId)
                .ToListAsync();
            if (courses == null || !courses.Any())
                return NotFound("No courses found for this department.");
            var courseDtos = courses.Select(c => new CourseInputDto
            {
                CourseId = c.CourseId,
                Name = c.Name,
                DepartmentId = c.DepartmentId,
                AverageCutoffRank = c.AverageCutoffRank,
                Fee = c.Fee,
                TotalSeats = c.TotalSeats,
                FacultyToStudentRatio = c.FacultyToStudentRatio,
                InternshipOpportunities = c.InternshipOpportunities,
                ScholarshipOffered = c.ScholarshipOffered,
                DurationInYears = c.DurationInYears,
                AdmissionProcess = c.AdmissionProcess,
                Rating = c.Rating
            }).ToList();
            return Ok(courseDtos);

        }

        // Get course details by course ID
        [HttpGet("GetCourseById/{courseId}")]
        public async Task<IActionResult> GetCourseById(int courseId)
        {
            var course = await _context.Courses.FindAsync(courseId);
            if (course == null)
                return NotFound("Course not found");
            var courseDto = new CourseInputDto
            {
                CourseId = course.CourseId,
                Name = course.Name,
                DepartmentId = course.DepartmentId,
                AverageCutoffRank = course.AverageCutoffRank,
                Fee = course.Fee,
                TotalSeats = course.TotalSeats,
                FacultyToStudentRatio = course.FacultyToStudentRatio,
                InternshipOpportunities = course.InternshipOpportunities,
                ScholarshipOffered = course.ScholarshipOffered,
                DurationInYears = course.DurationInYears,
                AdmissionProcess = course.AdmissionProcess,
                Rating = course.Rating
            };
            return Ok(courseDto);
        }

        // Update course details by course ID
        [HttpPut("UpdateCourse/{courseId}")]
        public async Task<IActionResult> UpdateCourse(int courseId, [FromBody] CourseInputDto dto)
        {
            var course = await _context.Courses.FindAsync(courseId);
            if (course == null)
                return NotFound("Course not found");
            course.Name = dto.Name;
            course.DepartmentId = dto.DepartmentId;
            course.AverageCutoffRank = dto.AverageCutoffRank;
            course.Fee = dto.Fee;
            course.TotalSeats = dto.TotalSeats;
            course.FacultyToStudentRatio = dto.FacultyToStudentRatio;
            course.InternshipOpportunities = dto.InternshipOpportunities;
            course.ScholarshipOffered = dto.ScholarshipOffered;
            course.DurationInYears = dto.DurationInYears;
            course.AdmissionProcess = dto.AdmissionProcess;
            course.Rating = dto.Rating;
            _context.Courses.Update(course);
            await _context.SaveChangesAsync();
            return Ok(new { message = "Course updated" });
        }

        //Delete course by course ID
        [HttpDelete("DeleteCourse/{courseId}")]
        public async Task<IActionResult> DeleteCourse(int courseId)
        {
            var course = await _context.Courses.FindAsync(courseId);
            if (course == null)
                return NotFound("Course not found");
            _context.Courses.Remove(course);
            await _context.SaveChangesAsync();
            return Ok(new { message = "Course deleted" });
        }
    }
}
