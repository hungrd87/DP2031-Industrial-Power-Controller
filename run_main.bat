@echo off
REM DP2031 Industrial Power Controller - Main Launcher
REM Simple batch script to run the application using main.py

echo ========================================
echo  DP2031 Industrial Power Controller
echo  Main Application Launcher  
echo ========================================

REM Check if virtual environment exists
if not exist ".venv" (
    echo ERROR: Virtual environment not found!
    echo Please run setup_venv.bat first
    pause
    exit /b 1
)

REM Activate virtual environment and run
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Starting DP2031 application...
python main.py %*

echo.
echo Application finished.
pause
