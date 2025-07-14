using Microsoft.AspNetCore.Mvc;

namespace CRSchatbotAPI.Controllers
{
    public class DepartmentController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}
