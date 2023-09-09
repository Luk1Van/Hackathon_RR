using Hackathon_RR.Models.HomeModels;
using Hackaton_RR.Models;
using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;
using System.Text.Json;

namespace Hackaton_RR.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;

        private readonly IConfiguration _configuration;

        public HomeController(ILogger<HomeController> logger, IConfiguration configuration)
        {
            _logger = logger;
            _configuration = configuration;
        }

        [HttpGet]
        public ViewResult Input(string firstTable)
        {
            InputModel inputModel = new InputModel()
            {
                testInput = "{\"stations\":[{\"Еманжелинск(1)\":[\"0\",\"38\",\"38\",\"25\",\"29\",\"7\",\"10\"]},{\"Омск(2)\":[\"0\",\"38\",\"38\",\"25\",\"29\",\"7\",\"10\"]}]}",
                firstTable = JsonSerializer.Serialize(firstTable)
            };
            return View(inputModel);
        }

        [HttpPost]
        public async Task<ActionResult>  Output()
        {
            OutputModel outputModel = new OutputModel()
            {

            };
            return View("Output");
        }


        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}