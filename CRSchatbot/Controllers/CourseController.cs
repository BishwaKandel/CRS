using CRSchatbotAPI.Data;
using CRSchatbotAPI.DTO;
using CRSchatbotAPI.Models;
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


        [HttpPost("CreateCourse")]
        public IActionResult CreateCourse([FromBody] CourseInputDto courseDto)
        {
            if (!ModelState.IsValid)
                return BadRequest(ModelState);

            // Map DTO to EF model
            var courseInDb = new Course
            {
                Name = courseDto.Name,
                DepartmentId = courseDto.DepartmentId,
                AverageCutoffRank = courseDto.AverageCutoffRank,
                Fee = courseDto.Fee,
                TotalSeats = courseDto.TotalSeats,
                FacultyToStudentRatio = courseDto.FacultyToStudentRatio,
                InternshipOpportunities = courseDto.InternshipOpportunities,
                ScholarshipOffered = courseDto.ScholarshipOffered,
                DurationInYears = courseDto.DurationInYears,
                AdmissionProcess = courseDto.AdmissionProcess,
                Rating = courseDto.Rating
            };

            _context.Courses.Add(courseInDb);
            _context.SaveChanges();

            return Ok(new { message = "Course created successfully", courseId = courseInDb.CourseId });
        }

    }
}
