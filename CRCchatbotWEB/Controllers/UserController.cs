using CRSchatbot.Shared.DTO;
using CRSchatbotAPI.DTO;
using Microsoft.AspNetCore.Mvc;
using System.Net.Http;

namespace CRSchatbotWEB.Controllers
{
    public class UserController : Controller
    {

        private readonly HttpClient client;
        public UserController(IHttpClientFactory httpClientFactory)
        {
            client = httpClientFactory.CreateClient("UserApi");
        }

        [HttpGet]
        public IActionResult Login()
        {
            return View();
        }


        [HttpPost]
        public async Task<IActionResult> Login(LoginViewModel model)
        {
            var response = await client.PostAsJsonAsync("login", new UserDto
            {
                Email = model.Email,
                Password = model.Password
            });

            if (response.IsSuccessStatusCode)
            {
                var result = await response.Content.ReadFromJsonAsync<LoginResponseDto>();

                // Store token and role in session
                HttpContext.Session.SetString("JWToken", result.Token);
                HttpContext.Session.SetString("UserRole", result.Role);
                HttpContext.Session.SetString("UserEmail", result.Email);
                HttpContext.Session.SetInt32("UserId", result.UserId);

                return RedirectToAction("Index", "Home");
            }

            ModelState.AddModelError("", "Invalid login");
            return View(model);
        }
        public IActionResult Logout()
        {
            HttpContext.Session.Clear(); // Clear everything
            return RedirectToAction("Login", "User"); // Go back to login page
        }


    }
}
