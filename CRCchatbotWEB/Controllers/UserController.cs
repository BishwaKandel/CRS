using CRSchatbot.Shared.DTO;
using CRSchatbotWEB.Models;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using System.Net.Http;
using System.Text;

namespace CRSchatbotWEB.Controllers
{
    public class UserController : Controller
    {

        private readonly HttpClient _httpClient;
        private readonly string _apiUrl;

        public UserController(HttpClient httpClient, IConfiguration configuration)
        {
            _httpClient = httpClient;
            _apiUrl = configuration["ApiSettings:BaseUrl"]; 
        }

        [HttpGet]
        public IActionResult Login()
        {
            return View();
        }

        [HttpPost]
        public async Task<IActionResult> Login(LoginViewModel model)
        {
            if (!ModelState.IsValid)
                return View(model);

            var json = JsonConvert.SerializeObject(model);
            var content = new StringContent(json, Encoding.UTF8, "application/json");

            var response = await _httpClient.PostAsync($"{_apiUrl}/login", content);

            if (response.IsSuccessStatusCode)
            {
                var responseContent = await response.Content.ReadAsStringAsync();
                var loginResult = JsonConvert.DeserializeObject<LoginResponseDto>(responseContent);

                HttpContext.Session.SetString("JWToken", loginResult.Token);
                HttpContext.Session.SetString("UserEmail", loginResult.Email);
                HttpContext.Session.SetString("UserRole", loginResult.Role);

                return RedirectToAction("Index", "Home");
            }
            else
            {
                ViewBag.LoginError = "Invalid email or password.";
                return View(model);
            }
        }

        [HttpGet]
        public IActionResult Register()
        {
            return View();
        }

        [HttpPost]
        public async Task<IActionResult> Register(RegisterViewModel model)
        {
            if (!ModelState.IsValid)
                return View(model);

            var json = JsonConvert.SerializeObject(model);
            var content = new StringContent(json, Encoding.UTF8, "application/json");

            var response = await _httpClient.PostAsync($"{_apiUrl}/register", content);

            if (response.IsSuccessStatusCode)
            {
                return RedirectToAction("Login", "User");
            }
            else
            {
                var error = await response.Content.ReadAsStringAsync();
                ModelState.AddModelError(string.Empty, error);
                return View(model);
            }
        }

        public IActionResult Logout()
        {
            HttpContext.Session.Clear();
            return RedirectToAction("Login", "User");
        }
    }
}

