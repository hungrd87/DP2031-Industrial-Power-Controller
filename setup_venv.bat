@echo off
REM DP2031 Industrial Power Controller - Virtual Environment Setup
REM This script creates a virtual environment and installs all dependencies

echo ============================================================
echo DP2031 Industrial Power Controller - Setup
echo ============================================================

cd /d "%~dp0"

echo Creating virtual environment...
python -m venv .venv

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Failed to create virtual environment!
    echo Please ensure Python 3.11+ is installed and accessible.
    pause
    exit /b 1
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing dependencies...
pip install -r requirements.txt

if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to install dependencies!
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo Testing installation...
python -c "import PyQt6; import numpy; import pyqtgraph; import pyvisa; print('All dependencies installed successfully!')"

if %ERRORLEVEL% neq 0 (
    echo ERROR: Dependency test failed!
    echo Some packages may not have installed correctly.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Setup completed successfully!
echo ============================================================
echo.
echo You can now run the application using:
echo   run_dp2031.bat
echo.
echo Or activate the environment manually:
echo   .venv\Scripts\activate.bat
echo   python -m dp2031_gui.app
echo ============================================================

pause
