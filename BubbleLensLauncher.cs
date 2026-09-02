using System;
using System.Diagnostics;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Windows.Forms;

namespace BubbleLensLauncher
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
                    if (IsBubbleLens())
                        StopStaleApp();
                    else
                        throw new InvalidOperationException("Local port 7873 is being used by another program. Close that program, then start BubbleLens again.");
                }

                if (!IsAppHealthy())
                {
                    if (!File.Exists(Path.Combine(BaseDir, "server.py")))
                        throw new FileNotFoundException("server.py was not found next to BubbleLens.exe.");
                    var python = FindPython();
                    if (python == null)
                        throw new FileNotFoundException("Python 3 was not found. Install Python 3.10 or newer, or set BUBBLELENS_PYTHON to python.exe.");
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
                MessageBox.Show("Startup failed:\n\n" + ex.Message, "BubbleLens", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private static Tuple<string, string> FindPython()
        {
            var configured = Environment.GetEnvironmentVariable("BUBBLELENS_PYTHON");
            if (String.IsNullOrWhiteSpace(configured)) configured = Environment.GetEnvironmentVariable("PROMPT_GENERATOR_PYTHON");
            if (!String.IsNullOrWhiteSpace(configured) && File.Exists(configured) && CanRunPython(configured, ""))
                return Tuple.Create(configured, "");

            var bundled = new[]
            {
                Path.Combine(BaseDir, "python", "python.exe"),
                Path.Combine(BaseDir, "runtime", "python.exe"),
                Path.Combine(BaseDir, "python.exe")
            };
            foreach (var candidate in bundled)
                if (File.Exists(candidate) && CanRunPython(candidate, "")) return Tuple.Create(candidate, "");

            // WindowsApps commonly exposes a python.exe placeholder that exits
            // immediately instead of running Python.  Prefer the real launcher,
            // and validate every PATH candidate before selecting it.
            var launcher = FindOnPath("py.exe", "-3 ");
            if (launcher != null) return Tuple.Create(launcher, "-3 ");
            var python = FindOnPath("python.exe", "");
            return python == null ? null : Tuple.Create(python, "");
        }

        private static bool CanRunPython(string executable, string prefix)
        {
            try
            {
                using (var process = Process.Start(new ProcessStartInfo
                {
                    FileName = executable,
                    Arguments = prefix + "--version",
                    UseShellExecute = false,
                    CreateNoWindow = true,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true
                }))
                {
                    if (process == null || !process.WaitForExit(3000))
                    {
                        if (process != null) process.Kill();
                        return false;
                    }
                    return process.ExitCode == 0;
                }
            }
            catch { return false; }
        }

        private static string FindOnPath(string executable, string prefix)
        {
            var path = Environment.GetEnvironmentVariable("PATH") ?? "";
            foreach (var part in path.Split(Path.PathSeparator))
            {
                var directory = part.Trim().Trim('"');
                if (directory.Length == 0) continue;
                try
                {
                    var candidate = Path.Combine(directory, executable);
                    if (File.Exists(candidate) && CanRunPython(candidate, prefix)) return candidate;
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

        private static bool IsBubbleLens()
        {
            var body = ReadHealth();
            return body != null && (body.Contains("\"app\":\"bubblelens\"") || body.Contains("\"app\":\"prompt-atelier\""));
        }

        private static bool IsAppHealthy()
        {
            var body = ReadHealth();
            // Catalog revisions do not make the local service incompatible with
            // this lightweight launcher.  Requiring one exact data version made
            // the v15 launcher reject and shut down the healthy v16 service.
            return body != null && body.Contains("\"app\":\"bubblelens\"");
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
                throw new InvalidOperationException("An older BubbleLens service could not be restarted. Close it and try again.");
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

        private static string GetProfilePath(string localData)
        {
            var currentRoot = Path.Combine(localData, "BubbleLens");
            var currentProfile = Path.Combine(currentRoot, "EdgeProfile");
            var legacyRoot = Path.Combine(localData, "PromptAtelier");
            var legacyProfile = Path.Combine(legacyRoot, "EdgeProfile");

            if (!Directory.Exists(currentRoot) && Directory.Exists(legacyProfile))
            {
                try
                {
                    Directory.Move(legacyRoot, currentRoot);
                }
                catch
                {
                    return legacyProfile;
                }
            }
            Directory.CreateDirectory(currentProfile);
            return currentProfile;
        }

        private static void OpenWindow()
        {
            var edge = System.IO.File.Exists(EdgeX86) ? EdgeX86 : Edge;
            if(System.IO.File.Exists(edge))
            {
                var localData = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
                var profile = GetProfilePath(localData);
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
