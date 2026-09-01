@echo off
cd /d "%~dp0"
set BUBBLELENS_NO_BROWSER=0
if defined BUBBLELENS_PYTHON (
  "%BUBBLELENS_PYTHON%" -B server.py
  exit /b %errorlevel%
)
where python >nul 2>nul
if not errorlevel 1 (
  python -B server.py
  exit /b %errorlevel%
)
where py >nul 2>nul
if not errorlevel 1 (
  py -3 -B server.py
  exit /b %errorlevel%
)
echo Python 3 was not found. Install Python 3.10 or newer.
pause
exit /b 1
