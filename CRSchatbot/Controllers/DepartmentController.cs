using CRSchatbotAPI.Data;
using CRSchatbotAPI.DTO;
using CRSchatbotAPI.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace CRSchatbotAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class DepartmentController : Controller
    {
        private readonly AppDbContext _context;

        public DepartmentController(AppDbContext context)
        {
            _context = context;
        }

        // Create a new department info
        [HttpPost("/colleges/{collegeId}/departments")]
        public async Task<IActionResult> AddDepartmentToCollege(int collegeId, [FromBody] CreateDepartmentDto dto)
        {
            var college = await _context.Colleges.FindAsync(collegeId);
            if (college == null)
                return NotFound("College not found");

            var department = new Department
            {
                Name = dto.Name,
                CollegeId = collegeId
            };

            _context.Departments.Add(department);
            await _context.SaveChangesAsync();

            return Ok(new { message = "Department added", departmentId = department.DepartmentId });
        }

        //Get all Departments by College ID 

        [HttpGet("/colleges/{collegeId}/departments")]
        public async Task<IActionResult> GetAllDepartmentsByCollege(int collegeId)
        {
            var college = await _context.Colleges
        .Include(c => c.Departments)
        .FirstOrDefaultAsync(c => c.CollegeId == collegeId);

            if (college == null)
                return NotFound("College not found");

            var departmentDtos = college.Departments.Select(d => new DepartmentDto
            {
                DepartmentId = d.DepartmentId,
                Name = d.Name
            }).ToList();
            return Ok(departmentDtos);
        }

        //	Get department details by department ID

        [HttpGet("/departments/{departmentId}")]
        public IActionResult GetDepartmentById(int departmentId)
        {
            var department = _context.Departments
                .Include(d => d.College)
                .FirstOrDefault(d => d.DepartmentId == departmentId);
            if (department == null)
                return NotFound("Department not found");
            var departmentDto = new DepartmentDto
            {
                DepartmentId = department.DepartmentId,
                Name = department.Name
            };
            return Ok(departmentDto);
        }

        // Update department details by department ID

        [HttpPut("/departments/{departmentId}")]
        public async Task<IActionResult> UpdateDepartment(int departmentId, [FromBody] CreateDepartmentDto dto)
        {
            var department = await _context.Departments.FindAsync(departmentId);
            if (department == null)
                return NotFound("Department not found");
            department.Name = dto.Name;
            _context.Departments.Update(department);
            await _context.SaveChangesAsync();
            return Ok(new { message = "Department updated" });
        }

        // Delete department by department ID
        [HttpDelete("/departments/{departmentId}")]
        public async Task<IActionResult> DeleteDepartment(int departmentId)
        {
            var department = await _context.Departments.FindAsync(departmentId);
            if (department == null)
                return NotFound("Department not found");
            _context.Departments.Remove(department);
            await _context.SaveChangesAsync();
            return Ok(new { message = "Department deleted" });

        }
    }
}
