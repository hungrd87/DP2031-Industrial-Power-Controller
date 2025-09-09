@echo off
REM DP2031 Debug Mode Launcher
REM Runs the application with debug logging enabled

echo ============================================================
echo DP2031 Industrial Power Controller - DEBUG MODE
echo ============================================================

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found!
    echo Please run setup_venv.bat first.
    pause
    exit /b 1
)

echo Starting DP2031 in DEBUG mode...
echo All debug information will be logged to console and files.
echo.

.venv\Scripts\python.exe -m dp2031_gui.app --debug

pause
