#!/usr/bin/env python3
"""
DP2031 Industrial Power Controller - Main Entry Point

Convenient entry point for running the DP2031 application directly.
This file provides easy access for development, debugging, and deployment.

Usage:
    python main.py                    # Normal mode
    python main.py --debug            # Debug mode
    python main.py --demo             # Demo mode (simulation)
    python main.py --help             # Show help

Author: Industrial Control Systems
Version: 1.0.0
Date: September 9, 2025
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Main entry point for DP2031 application."""
    
    # Print startup banner
    print("=" * 60)
    print("🔋 DP2031 Industrial Power Controller")
    print("   Professional RIGOL DP2000/DP2031 Controller")
    print("=" * 60)
    print(f"📁 Project Root: {project_root}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print("-" * 60)
    
    try:
        # Import and run the application
        from dp2031_gui.app import main as app_main
        
        print("🚀 Starting application...")
        return app_main()
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("\n💡 Possible solutions:")
        print("   1. Check virtual environment is activated")
        print("   2. Install dependencies: pip install -r requirements.txt")
        print("   3. Run setup script: setup_venv.bat")
        return 1
        
    except KeyboardInterrupt:
        print("\n⏹️  Application interrupted by user")
        return 0
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("\n🔍 For detailed debugging, run with:")
        print("   python main.py --debug")
        return 1


def check_environment():
    """Check if the environment is properly set up."""
    
    print("🔍 Environment Check:")
    
    # Check virtual environment
    venv_path = project_root / ".venv"
    if venv_path.exists():
        print(f"   ✅ Virtual environment found: {venv_path}")
    else:
        print(f"   ⚠️  Virtual environment not found: {venv_path}")
        print("      Run 'setup_venv.bat' to create it")
    
    # Check requirements file
    req_path = project_root / "requirements.txt"
    if req_path.exists():
        print(f"   ✅ Requirements file found: {req_path}")
    else:
        print(f"   ❌ Requirements file missing: {req_path}")
    
    # Check main package
    package_path = project_root / "dp2031_gui"
    if package_path.exists():
        print(f"   ✅ Main package found: {package_path}")
    else:
        print(f"   ❌ Main package missing: {package_path}")
    
    print("-" * 60)


def show_help():
    """Show usage help."""
    
    help_text = """
🔋 DP2031 Industrial Power Controller - Usage Guide

BASIC USAGE:
    python main.py                    # Start application normally
    python main.py --debug            # Start with debug logging
    python main.py --demo             # Start in demo/simulation mode
    
ADVANCED OPTIONS:
    python main.py --log-level DEBUG  # Set specific log level
    python main.py --resource USB0::  # Specify VISA resource pattern
    python main.py --no-splash        # Disable splash screen
    
DEVELOPMENT:
    python main.py --help             # Show this help
    python -m pytest tests/           # Run test suite
    python -m dp2031_gui.app --debug  # Direct module execution
    
BATCH SCRIPTS (Windows):
    run_app.bat                       # Quick start script
    run_debug.bat                     # Debug mode script
    run_tests.bat                     # Test runner script
    setup_venv.bat                    # Environment setup
    
FEATURES:
    ✅ 3-Channel Power Supply Control
    ✅ Real-time Monitoring & Trending
    ✅ Industrial GUI with Big Digits
    ✅ Protection & Alarm Management
    ✅ Data Logging & Export
    ✅ VISA Communication (USB/LAN/RS232)
    
SUPPORTED DEVICES:
    • RIGOL DP2000 Series
    • RIGOL DP2031 Power Supply
    • Compatible SCPI instruments
    
For more information, see README.md
"""
    print(help_text)


if __name__ == "__main__":
    
    # Handle help request
    if "--help" in sys.argv or "-h" in sys.argv:
        show_help()
        sys.exit(0)
    
    # Handle environment check
    if "--check" in sys.argv:
        check_environment()
        sys.exit(0)
    
    # Check environment before running
    check_environment()
    
    # Run the application
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⏹️  Goodbye!")
        sys.exit(0)
