using Hackathon_RR.Data;
using Hackathon_RR.MLintegration;
using Hackathon_RR.Models.HomeModels;
using Hackaton_RR.Models;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using System.Diagnostics;


namespace Hackaton_RR.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;

        private readonly IConfiguration _configuration;
        private readonly IMLintegration _mLintegration;

        public HomeController(ILogger<HomeController> logger, IConfiguration configuration, IMLintegration mLintegration)
        {
            _logger = logger;
            _configuration = configuration;
            _mLintegration = mLintegration;
        }

        [HttpGet]
        public ViewResult Input()
        {
            ViewBag.testInput = "{\"stations\":[{\"Еманжелинск(1)\":[\"0\",\"38\",\"38\",\"25\",\"29\",\"7\",\"10\"]},{\"Омск(2)\":[\"0\",\"38\",\"38\",\"25\",\"29\",\"7\",\"10\"]}]}";
            ViewBag.exampleInput = "{\"563\":{\"free_carriage\":[\"33\",\"20\",\"35\",\"3\"]}}";
            return View();
        }

        

        [HttpPost]
        public async Task<ActionResult>  Output()
        {
            Data _data = new Data();
            string json = _data.jsonResult;

            Dictionary<string, OutputModel> jsonData = JsonConvert.DeserializeObject<Dictionary<string, OutputModel>>(json);
            
            return View(jsonData);
        }


        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}