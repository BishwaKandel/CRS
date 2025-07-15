using CRSchatbotAPI.Data;
using CRSchatbotAPI.DTO;
using CRSchatbotAPI.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace CRSchatbotAPI.Controllers
{
    public class CinfoContentController : Controller
    {
        private readonly AppDbContext _context;

        public CinfoContentController(AppDbContext context)
        {
            _context = context;
        }

        //Create Content 
        [HttpPost("/colleges/{collegeId}/content")]
        public async Task<IActionResult> CreateContent(int collegeId, [FromBody] CollegeInfoContentInputDto dto)
        {
            var college = await _context.Colleges.FindAsync(collegeId);
            if (college == null)
                return NotFound("College not found");

            // Parse the ContentType from string to enum
            if (!Enum.TryParse<ContentType>(dto.Type, out var parsedType))
                return BadRequest("Invalid content type");

            var content = new CollegeInfoContent
            {
                Name = dto.Name,
                Title = dto.Title,
                Description = dto.Description,
                Body = dto.Body,
                Type = parsedType,
                CreatedAt = dto.CreatedAt,
                CreatedById = dto.CreatedById,
                CollegeId = collegeId, // override if passed in URL
                DepartmentId = dto.DepartmentId,
                CourseId = dto.CourseId
            };

            _context.CollegeInfoContents.Add(content);
            await _context.SaveChangesAsync();

            return Ok(new { message = "Content created", contentId = content.Id });
        }

        // Get all content for a college
        [HttpGet("/colleges/{collegeId}/content")]
        public async Task<IActionResult> GetContentByCollege(int collegeId)
        {
            var contentList = await _context.CollegeInfoContents
                .Where(c => c.CollegeId == collegeId)
                .ToListAsync();
            if (contentList == null || !contentList.Any())
                return NotFound("No content found for this college.");
            return Ok(contentList);
        }

        //Get content by ID
        [HttpGet("/content/{id}")]
        public async Task<IActionResult> GetContentById(int id)
        {
            var content = await _context.CollegeInfoContents.FindAsync(id);
            if (content == null)
                return NotFound($"Content with ID {id} not found.");
            return Ok(content);
        }

        // Get all content by department ID
        [HttpGet("/departments/{departmentId}/content")]
        public async Task<IActionResult> GetContentByDepartment(int departmentId)
        {
            var contentList = await _context.CollegeInfoContents
                .Where(c => c.DepartmentId == departmentId)
                .ToListAsync();
            if (contentList == null || !contentList.Any())
                return NotFound("No content found for this department.");
            return Ok(contentList);
        }

        //Get all content by course ID
        [HttpGet("/courses/{courseId}/content")]
        public async Task<IActionResult> GetContentByCourse(int courseId)
        {
            var contentList = await _context.CollegeInfoContents
                .Where(c => c.CourseId == courseId)
                .ToListAsync();
            if (contentList == null || !contentList.Any())
                return NotFound("No content found for this course.");
            return Ok(contentList);
        }


        // Update content by ID
        [HttpPut("/content/{id}")]
        public async Task<IActionResult> UpdateContent(int id, [FromBody] CollegeInfoContentInputDto dto)
        {
            var content = await _context.CollegeInfoContents.FindAsync(id);
            if (content == null)
                return NotFound($"Content with ID {id} not found.");
            // Parse the ContentType from string to enum
            if (!Enum.TryParse<ContentType>(dto.Type, out var parsedType))
                return BadRequest("Invalid content type");
            content.Name = dto.Name;
            content.Title = dto.Title;
            content.Description = dto.Description;
            content.Body = dto.Body;
            content.Type = parsedType;
            content.CreatedAt = dto.CreatedAt;
            content.CreatedById = dto.CreatedById;
            content.DepartmentId = dto.DepartmentId;
            content.CourseId = dto.CourseId;
            _context.CollegeInfoContents.Update(content);
            await _context.SaveChangesAsync();
            return Ok(new { message = "Content updated", content });
        }

        // Delete content by ID
        [HttpDelete("/content/{id}")]
        public async Task<IActionResult> DeleteContent(int id)
        {
            var content = await _context.CollegeInfoContents.FindAsync(id);
            if (content == null)
                return NotFound($"Content with ID {id} not found.");
            _context.CollegeInfoContents.Remove(content);
            await _context.SaveChangesAsync();
            return Ok(new { message = "Content deleted" });


        }
    }
}
