using System;
using System.Diagnostics;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Windows.Forms;

namespace PromptGeneratorLauncher
{
    internal static class Program
    {
        private static readonly string BaseDir = AppDomain.CurrentDomain.BaseDirectory.TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar);
        private const string Url = "http://127.0.0.1:7873";
        private const string EdgeX86 = @"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe";
        private const string Edge = @"C:\Program Files\Microsoft\Edge\Application\msedge.exe";

        [STAThread]
        private static void Main()
        {
            Application.EnableVisualStyles();
            try
            {
                if (IsPortOpen(7873) && !IsAppHealthy())
                {
                    if (IsPromptApp())
                        StopStaleApp();
                    else
                        throw new InvalidOperationException("Local port 7873 is being used by another program. Close that program, then start Prompt Generator again.");
                }

                if (!IsAppHealthy())
                {
                    if (!File.Exists(Path.Combine(BaseDir, "server.py")))
                        throw new FileNotFoundException("server.py was not found next to PromptGenerator.exe.");
                    var python = FindPython();
                    if (python == null)
                        throw new FileNotFoundException("Python 3 was not found. Install Python 3.10 or newer, or set PROMPT_GENERATOR_PYTHON to python.exe.");
                    var info = new ProcessStartInfo
                    {
                        FileName = python.Item1,
                        Arguments = python.Item2 + "-B \"" + BaseDir + "\\server.py\" --no-browser",
                        WorkingDirectory = BaseDir,
                        UseShellExecute = false,
                        CreateNoWindow = true,
                        WindowStyle = ProcessWindowStyle.Hidden
                    };
                    Process.Start(info);
                }
                WaitForApp(30);
                OpenWindow();
            }
            catch (Exception ex)
            {
                MessageBox.Show("Startup failed:\n\n" + ex.Message, "Prompt Generator", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private static Tuple<string, string> FindPython()
        {
            var configured = Environment.GetEnvironmentVariable("PROMPT_GENERATOR_PYTHON");
            if (!String.IsNullOrWhiteSpace(configured) && File.Exists(configured))
                return Tuple.Create(configured, "");

            var bundled = new[]
            {
                Path.Combine(BaseDir, "python", "python.exe"),
                Path.Combine(BaseDir, "runtime", "python.exe"),
                Path.Combine(BaseDir, "python.exe")
            };
            foreach (var candidate in bundled)
                if (File.Exists(candidate)) return Tuple.Create(candidate, "");

            var python = FindOnPath("python.exe");
            if (python != null) return Tuple.Create(python, "");
            var launcher = FindOnPath("py.exe");
            return launcher == null ? null : Tuple.Create(launcher, "-3 ");
        }

        private static string FindOnPath(string executable)
        {
            var path = Environment.GetEnvironmentVariable("PATH") ?? "";
            foreach (var part in path.Split(Path.PathSeparator))
            {
                var directory = part.Trim().Trim('"');
                if (directory.Length == 0) continue;
                try
                {
                    var candidate = Path.Combine(directory, executable);
                    if (File.Exists(candidate)) return candidate;
                }
                catch { }
            }
            return null;
        }

        private static string ReadHealth()
        {
            try
            {
                var request = (HttpWebRequest)WebRequest.Create(Url + "/api/health");
                request.Timeout = 700;
                request.ReadWriteTimeout = 700;
                request.Proxy = null;
                using (var response = (HttpWebResponse)request.GetResponse())
                using (var reader = new StreamReader(response.GetResponseStream()))
                {
                    return response.StatusCode == HttpStatusCode.OK ? reader.ReadToEnd() : null;
                }
            }
            catch { return null; }
        }

        private static bool IsPromptApp()
        {
            var body = ReadHealth();
            return body != null && body.Contains("\"app\":\"prompt-atelier\"");
        }

        private static bool IsAppHealthy()
        {
            var body = ReadHealth();
            return body != null && body.Contains("\"app\":\"prompt-atelier\"") && body.Contains("\"version\":14");
        }

        private static void StopStaleApp()
        {
            try
            {
                var request = (HttpWebRequest)WebRequest.Create(Url + "/api/shutdown");
                request.Method = "POST";
                request.Timeout = 1000;
                request.Proxy = null;
                using (request.GetResponse()) { }
            }
            catch { }
            for (var i = 0; i < 20 && IsPortOpen(7873); i++) Thread.Sleep(100);
            if (IsPortOpen(7873))
                throw new InvalidOperationException("An older Prompt Generator service could not be restarted. Close it and try again.");
        }

        private static bool IsPortOpen(int port)
        {
            try { using (var c = new TcpClient()) { var r=c.BeginConnect("127.0.0.1",port,null,null); if(!r.AsyncWaitHandle.WaitOne(400))return false; c.EndConnect(r); return true; } }
            catch { return false; }
        }

        private static void WaitForApp(int seconds)
        {
            for(var i=0;i<seconds*4;i++){if(IsAppHealthy())return;Thread.Sleep(250);}
            throw new TimeoutException("The local service timed out while starting.");
        }

        private static void OpenWindow()
        {
            var edge = System.IO.File.Exists(EdgeX86) ? EdgeX86 : Edge;
            if(System.IO.File.Exists(edge))
            {
                var localData = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
                var profile = System.IO.Path.Combine(localData, "PromptAtelier", "EdgeProfile");
                System.IO.Directory.CreateDirectory(profile);
                Process.Start(new ProcessStartInfo
                {
                    FileName=edge,
                    Arguments="--app=\""+Url+"\" --start-maximized --no-first-run --disable-sync --user-data-dir=\""+profile+"\"",
                    UseShellExecute=true
                });
                return;
            }
            Process.Start(new ProcessStartInfo{FileName=Url,UseShellExecute=true});
        }
    }
}
