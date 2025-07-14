using Microsoft.AspNetCore.Mvc;

namespace CRSchatbotAPI.Controllers
{
    public class CourseController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}
