using Microsoft.AspNetCore.Mvc;

namespace CRSchatbotAPI.Controllers
{
    public class CollegeController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}
