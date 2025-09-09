@echo off
REM Test runner script for DP2031 Industrial Power Controller
REM Runs all tests with coverage reporting and detailed output

echo ========================================
echo DP2031 Industrial Power Controller Tests
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

REM Verify pytest is installed
python -c "import pytest" 2>nul
if errorlevel 1 (
    echo Installing pytest...
    pip install pytest pytest-cov pytest-mock
)

echo.
echo Running unit tests...
echo ========================

REM Run tests with coverage
python -m pytest tests/ -v --tb=short --cov=dp2031_gui --cov-report=term-missing --cov-report=html:htmlcov

echo.
echo ========================
echo Test Results Summary
echo ========================

REM Check test results
if errorlevel 1 (
    echo.
    echo [FAILED] Some tests failed. Please check the output above.
    echo.
) else (
    echo.
    echo [PASSED] All tests completed successfully!
    echo.
    echo Coverage report generated in: htmlcov\index.html
    echo.
)

REM Keep window open
echo Press any key to exit...
pause >nul
