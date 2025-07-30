using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using CRSchatbot.Shared.Models;

namespace CRSchatbotWEB.Controllers
{
    public class CollegeController : Controller
    {
        private readonly HttpClient _httpClient;
        private readonly string _apiUrl = "https://localhost:7228/api/College";

        public CollegeController()
        {
            _httpClient = new HttpClient();
        }

        public async Task<IActionResult> Index()
        {
            List<College> colleges = new List<College>();

            var response = await _httpClient.GetAsync($"{_apiUrl}/getcolleges");

            if (response.IsSuccessStatusCode)
            {
                var result = await response.Content.ReadAsStringAsync();
                colleges = JsonConvert.DeserializeObject<List<College>>(result);
            }
            else
            {
                ModelState.AddModelError(string.Empty, "Unable to fetch data from API.");
            }

            return View(colleges);
        }
        public async Task<IActionResult> Details()
        {
            return View();
        }

    }
}
