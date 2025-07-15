using CRSchatbotAPI.Data;
using CRSchatbotAPI.DTO;
using CRSchatbotAPI.Models;
using Microsoft.AspNetCore.Mvc;

namespace CRSchatbotAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class CollegeController : Controller
    {
        private readonly AppDbContext _context;

        public CollegeController(AppDbContext context)
        {
            _context = context;
        }
        //Create a new college info

        [HttpPost("getcollegeinfo")]
        public IActionResult GetCollegeInfo([FromBody] CollegeInputDto collegeDto)
        {
            if (!ModelState.IsValid)
                return BadRequest(ModelState);

            // Map DTO to EF entity
            //var college = new College
            //{
            //    Name = collegeDto.Name,
            //    Location = collegeDto.Location,
            //    Type = collegeDto.Type,
            //    ContactNumber = collegeDto.ContactNumber,
            //    Email = collegeDto.Email,
            //    HostelAvailability = collegeDto.HostelAvailability,
            //    Departments = collegeDto.Departments.Select(d => new Department
            //    {
            //        Name = d.Name,
            //        CollegeId = 0, // Will be assigned after saving college if using EF Core
            //        Courses = d.Courses.Select(c => new Course
            //        {
            //            Name = c.Name,
            //            AverageCutoffRank = c.AverageCutoffRank,
            //            Fee = c.Fee,
            //            DepartmentId = 0, // will be assigned by EF Core
            //            TotalSeats = c.TotalSeats,
            //            FacultyToStudentRatio = c.FacultyToStudentRatio,
            //            InternshipOpportunities = c.InternshipOpportunities,
            //            ScholarshipOffered = c.ScholarshipOffered,
            //            DurationInYears = c.DurationInYears,
            //            AdmissionProcess = c.AdmissionProcess,
            //            Rating = c.Rating
            //        }).ToList()
            //    }).ToList()
            //};
            var college = new College
            {
                Name = collegeDto.Name,
                Location = collegeDto.Location,
                Type = collegeDto.Type,
                ContactNumber = collegeDto.ContactNumber,
                Email = collegeDto.Email,
                HostelAvailability = collegeDto.HostelAvailability,
                Departments = collegeDto.Departments?.Select(d => new Department
                {
                    Name = d.Name,
                    Courses = d.Courses?.Select(c => new Course
                    {
                        Name = c.Name,
                        AverageCutoffRank = c.AverageCutoffRank,
                        Fee = c.Fee,
                        TotalSeats = c.TotalSeats,
                        FacultyToStudentRatio = c.FacultyToStudentRatio,
                        InternshipOpportunities = c.InternshipOpportunities,
                        ScholarshipOffered = c.ScholarshipOffered,
                        DurationInYears = c.DurationInYears,
                        AdmissionProcess = c.AdmissionProcess,
                        Rating = c.Rating
                    }).ToList() ?? new List<Course>()
                }).ToList() ?? new List<Department>()
            };


            // Check for duplicates, save to database, etc.
            _context.Colleges.Add(college);
            _context.SaveChanges();

            return Ok(new { Message = "College info added", college });
        }

        //public IActionResult Index()
        //{
        //    return View();
        //}
    }
}
