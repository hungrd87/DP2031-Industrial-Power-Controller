@echo off
REM DP2031 Industrial Power Controller - Debug Launcher
REM Batch script for easy debugging using debug.py

echo ========================================
echo  DP2031 DEBUG MODE
echo  Enhanced Debugging Session
echo ========================================

REM Check if virtual environment exists
if not exist ".venv" (
    echo ERROR: Virtual environment not found!
    echo Please run setup_venv.bat first
    pause
    exit /b 1
)

REM Activate virtual environment and run debug
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Starting debug session...
python debug.py %*

echo.
echo Debug session finished.
pause
