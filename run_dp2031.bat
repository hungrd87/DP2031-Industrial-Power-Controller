@echo off
REM DP2031 Industrial Power Controller - Application Launcher
REM This script runs the DP2031 control application

echo ============================================================
echo DP2031 Industrial Power Controller
echo RIGOL DP2000/DP2031 Power Supply Control
echo ============================================================

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found!
    echo Please run setup_venv.bat first to create the environment.
    echo.
    pause
    exit /b 1
)

echo Starting DP2031 Industrial Power Controller...
echo.
echo Connect your RIGOL DP2000/DP2031 via:
echo   - USB: Connect USB cable
echo   - LAN: Configure IP address and ensure VXI-11 protocol
echo   - RS232: Connect serial cable and configure port settings
echo.

.venv\Scripts\python.exe -m dp2031_gui.app

if %ERRORLEVEL% neq 0 (
    echo.
    echo Application exited with error code %ERRORLEVEL%
    echo Check logs/dp2031_app.log for detailed error information.
    echo.
)

pause
