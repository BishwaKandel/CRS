using CRSchatbot.Shared.DTO;
using CRSchatbotAPI.Data;
using CRSchatbotAPI.DTO;
using CRSchatbotAPI.Models;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;

namespace CRSchatbotAPI.Services
{
    public class AuthService : IAuthService
    {
        private readonly IConfiguration configuration;
        private readonly AppDbContext context;

        public AuthService(IConfiguration configuration, AppDbContext context)
        {
            this.configuration = configuration;
            this.context = context;
            Console.WriteLine("AuthService constructed");
        }
        public async Task<User?> RegisterAsync(UserDto request)
        {
            if (context.Users.Any(u => u.Email == request.Email))
            {
                return null; // User already exists
            }
            var user = new User();
            user.Email = request.Email;
            user.PasswordHash = new PasswordHasher<User>()
                .HashPassword(user, request.Password);
            user.FullName = request.FullName;
            await context.Users.AddAsync(user);
            await context.SaveChangesAsync();
            return user;
        }
        public async Task<LoginResponseDto?> LoginAsync(UserDto request)
        {
            User? user = await context.Users.FirstOrDefaultAsync(u => u.Email == request.Email);

            if (user is null || user.PasswordHash == null ||
                new PasswordHasher<User>().VerifyHashedPassword(user, user.PasswordHash, request.Password)
                != PasswordVerificationResult.Success)
            {
                return null;
            }

            string token = CreateToken(user);

            return new LoginResponseDto
            {
                Token = token,
                Role = user.Role,
                Email = user.Email,
                UserId = user.Id
            };
        }

        private string CreateToken(User user)
        {
            var claims = new List<Claim>
                    {
                        new Claim(ClaimTypes.Email, user.Email),
                        new Claim(ClaimTypes.NameIdentifier, user.Id.ToString()),
                        new Claim(ClaimTypes.Role, user.Role),
                    };
            var key = new SymmetricSecurityKey(System.Text.Encoding.UTF8.GetBytes(configuration["Jwt:Key"]));
            var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);
            var token = new JwtSecurityToken(
                issuer: configuration["Jwt:Issuer"],
                audience: configuration["Jwt:Audience"],
                claims: claims,
                expires: DateTime.Now.AddMinutes(60),
                signingCredentials: creds
            );
            return new JwtSecurityTokenHandler().WriteToken(token);
        }
    }
}
