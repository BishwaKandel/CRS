using Microsoft.EntityFrameworkCore;
using CRSchatbot.Shared.Models;

namespace CRSchatbotAPI.Data
{
    public class AppDbContext : DbContext
    {
        public DbSet<College> Colleges { get; set; } = null;
        public DbSet<Course> Courses { get; set; } = null;
        public DbSet<Department> Departments { get; set; } = null;

        public DbSet<User> Users { get; set; } = null;
        public DbSet<CollegeInfoContent> CollegeInfoContents { get; set; } = null;

        public AppDbContext(DbContextOptions<AppDbContext> options)
            : base(options)
        {

        }
    }
}
