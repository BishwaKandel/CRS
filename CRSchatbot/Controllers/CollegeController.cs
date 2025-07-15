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
        ////Create a new college info

        [HttpPost("CreateCollege")]
        public IActionResult CreateCollege([FromBody] CollegeInputDto collegeDto)
        {
            if (!ModelState.IsValid)
                return BadRequest(ModelState);

            // Map DTO to EF entity
            var college = new College
            {
                Name = collegeDto.Name,
                Location = collegeDto.Location,
                Type = collegeDto.Type,
                ContactNumber = collegeDto.ContactNumber,
                Email = collegeDto.Email,
                HostelAvailability = collegeDto.HostelAvailability,
                Departments = collegeDto.Departments.Select(d => new Department
                {
                    Name = d.Name,
                    CollegeId = 0, // Will be assigned after saving college if using EF Core
                    Courses = d.Courses.Select(c => new Course
                    {
                        Name = c.Name,
                        AverageCutoffRank = c.AverageCutoffRank,
                        Fee = c.Fee,
                        DepartmentId = 0, // will be assigned by EF Core
                        TotalSeats = c.TotalSeats,
                        FacultyToStudentRatio = c.FacultyToStudentRatio,
                        InternshipOpportunities = c.InternshipOpportunities,
                        ScholarshipOffered = c.ScholarshipOffered,
                        DurationInYears = c.DurationInYears,
                        AdmissionProcess = c.AdmissionProcess,
                        Rating = c.Rating
                    }).ToList()
                }).ToList()
            };
            //var college = new College
            //{
            //    Name = collegeDto.Name,
            //    Location = collegeDto.Location,
            //    Type = collegeDto.Type,
            //    ContactNumber = collegeDto.ContactNumber,
            //    Email = collegeDto.Email,
            //    HostelAvailability = collegeDto.HostelAvailability,
            //    Departments = collegeDto.Departments?.Select(d => new Department
            //    {
            //        Name = d.Name,
            //        Courses = d.Courses?.Select(c => new Course
            //        {
            //            Name = c.Name,
            //            AverageCutoffRank = c.AverageCutoffRank,
            //            Fee = c.Fee,
            //            TotalSeats = c.TotalSeats,
            //            FacultyToStudentRatio = c.FacultyToStudentRatio,
            //            InternshipOpportunities = c.InternshipOpportunities,
            //            ScholarshipOffered = c.ScholarshipOffered,
            //            DurationInYears = c.DurationInYears,
            //            AdmissionProcess = c.AdmissionProcess,
            //            Rating = c.Rating
            //        }).ToList() ?? new List<Course>()
            //    }).ToList() ?? new List<Department>()
            //};


            // Check for duplicates, save to database, etc.
            _context.Colleges.Add(college);
            _context.SaveChanges();

            return Ok(new { Message = "College info added", college });
        }

        [HttpGet("getcolleges")]
        public IActionResult GetColleges()
        {
            var collegeinDB = _context.Colleges.ToList();
            if (collegeinDB == null || !collegeinDB.Any())
            {
                return NotFound("No colleges found.");
            }

            return Ok(collegeinDB);
        }

        //Get College by ID
        [HttpGet("getcolleges{id}")]
        public IActionResult GetCollegebyID(int id)
        {
            var collegeinDB = _context.Colleges.Find(id);

            if (collegeinDB == null )
            {
                return NotFound($"College with ID {id} not found");
            }
            return Ok(collegeinDB);
        }

        //Update College Info by ID 

        [HttpPut("updatecolleges{id}")]
        public IActionResult UpdateCollegeInfo(int id , [FromBody] CollegeUpdateDto  updatedCollege)
        {
            var collegeinDB = _context.Colleges.Find(id);

            if (collegeinDB == null)
            {
                return NotFound($"College with CollegeID {id} is not found");
            }

            collegeinDB.Name = updatedCollege.Name;
            collegeinDB.Location = updatedCollege.Location;
            collegeinDB.Type = updatedCollege.Type;
            collegeinDB.ContactNumber = updatedCollege.ContactNumber;
            collegeinDB.Email = updatedCollege.Email;
            collegeinDB.HostelAvailability = updatedCollege.HostelAvailability;

            _context.SaveChanges();

            return Ok(collegeinDB);
        }

        //Delete College

        [HttpDelete("deletecolleges{id}")]

        public IActionResult DeleteCollege(int id)
        {
            var collegeinDB = _context.Colleges.Find(id);

            if (collegeinDB == null )
                return NotFound($"College with CollegeID {id} is not found");

            _context.Colleges.Remove(collegeinDB);
            _context.SaveChanges();
            return Ok(collegeinDB);
        }
    }
}

