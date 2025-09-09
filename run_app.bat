@echo off
REM Quick launcher for DP2031 Industrial Power Controller
REM This script activates the virtual environment and runs the application

echo ========================================
echo DP2031 Industrial Power Controller
echo ========================================
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo ERROR: Virtual environment not found!
    echo Please run setup_venv.bat first to create the environment.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Check if main application exists
if not exist "dp2031_gui\app.py" (
    echo ERROR: Application files not found!
    echo Please ensure dp2031_gui\app.py exists.
    echo.
    pause
    exit /b 1
)

echo.
echo Starting DP2031 Industrial Power Controller...
echo.

REM Run the application
python -m dp2031_gui.app

REM Check exit code
if errorlevel 1 (
    echo.
    echo Application exited with error code: %errorlevel%
    echo Check the logs for more information.
    echo.
    pause
)

echo.
echo Application closed.
pause
