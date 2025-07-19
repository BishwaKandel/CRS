namespace CRSchatbotAPI.Models
{
    public class User
    {
        public int Id { get; set; }

        // Auth
        public string Email { get; set; } = string.Empty;
        public string PasswordHash { get; set; } = string.Empty;

        // Identity
        public string FullName { get; set; } = string.Empty;
        public string Role { get; set; } = string.Empty;// "Admin" or "Student"

        // Activity
        public DateTime CreatedAt { get; set; } 
        public DateTime LastLogin { get; set; }
    }
}
