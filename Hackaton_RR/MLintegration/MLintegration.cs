using System;
using System.IO;
using System.Diagnostics;
using Microsoft.AspNetCore.Components.Forms;

namespace Hackathon_RR.MLintegration
{
    public class MLintegration : IMLintegration
    {
        public string runMl(string inputText)
        {

            Process p = new Process();
            p.StartInfo = new ProcessStartInfo()
            {
                FileName = "D:\\Python\\python.exe",
                Arguments = "D:\\PythonTest\\test_script.py --text \"" + inputText + "\\",
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };
            p.Start();

            string output = p.StandardOutput.ReadToEnd();
            p.WaitForExit();

            return output;
        }

    }
}
