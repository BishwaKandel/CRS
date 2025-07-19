using CRSchatbot.Shared.DTO;
using CRSchatbotAPI.DTO;
using CRSchatbotAPI.Models;
using CRSchatbotAPI.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;

namespace CRSchatbotAPI.Controllers
{
    
    [Route("api/[controller]")]
    [ApiController]

    public class UserController : Controller
    {
        private readonly IAuthService service;
        public UserController(IAuthService service)
        {
            this.service = service;
        }

        [HttpPost("register")]
        public async Task<ActionResult<User?>> Register(UserDto request)
        {

            var user = await service.RegisterAsync(request);
            if (user is null)
            {
                return BadRequest("User already exists.");
            }
            return Ok(new UserProfileDto
            {
                Email = user.Email,
                FullName = user.FullName,
                Role = user.Role
            });

        }

        [HttpPost("login")]
        public async Task<ActionResult<LoginResponseDto>> Login(UserDto request)
        {
            var response = await service.LoginAsync(request);

            if (response is null)
            {
                return BadRequest("Invalid email or password.");
            }

            return Ok(response);
        }

    }





}
