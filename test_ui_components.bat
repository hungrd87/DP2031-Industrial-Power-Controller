@echo off
REM Test script for DP2031 UI components
REM Validates that all UI components can be imported and created

echo ========================================
echo DP2031 UI Components Test
echo ========================================
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo ERROR: Virtual environment not found!
    echo Please run setup_venv.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Testing UI components...
echo.

REM Run UI component test
python test_ui.py

REM Check result
if errorlevel 1 (
    echo.
    echo [FAILED] UI component test failed!
    echo Please check error messages above.
    echo.
) else (
    echo.
    echo [PASSED] All UI components working correctly!
    echo.
)

echo Press any key to exit...
pause >nul
