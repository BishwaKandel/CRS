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
        public UserController(IAuthService service)
        {
            this.service = service;
        }
        private readonly IAuthService service;

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
        public async Task<ActionResult<string>> LoginAsync(UserDto request)
        {
            var token = await service.LoginAsync(request);


            if (token is null)
            {
                return BadRequest("Invalid email or password.");
            }
            return Ok(token);
        }



    }
}
