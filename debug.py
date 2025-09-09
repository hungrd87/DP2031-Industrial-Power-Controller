#!/usr/bin/env python3
"""
DP2031 Industrial Power Controller - Debug Entry Point

Specialized entry point for debugging the DP2031 application.
Provides enhanced logging, error handling, and development tools.

Usage:
    python debug.py                  # Debug mode with full logging
    python debug.py --verbose        # Extra verbose output
    python debug.py --profile        # Enable performance profiling
    python debug.py --mock           # Mock hardware mode

Author: Industrial Control Systems
Version: 1.0.0
Date: September 9, 2025
"""

import sys
import os
import time
import traceback
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def debug_banner():
    """Print debug session banner."""
    print("=" * 70)
    print("🐛 DP2031 DEBUG MODE")
    print("   Enhanced Debugging & Development Tools")
    print("=" * 70)
    print(f"📁 Project Root: {project_root}")
    print(f"🐍 Python: {sys.version}")
    print(f"⏰ Session Start: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔧 Debug Args: {sys.argv[1:] if len(sys.argv) > 1 else 'None'}")
    print("-" * 70)

def check_debug_environment():
    """Enhanced environment check for debugging."""
    
    print("🔍 DEBUG ENVIRONMENT CHECK:")
    
    issues = []
    
    # Check Python version
    if sys.version_info < (3, 11):
        issues.append(f"⚠️  Python version {sys.version_info} may be too old")
    else:
        print(f"   ✅ Python version: {sys.version_info}")
    
    # Check virtual environment
    venv_path = project_root / ".venv"
    if venv_path.exists():
        print(f"   ✅ Virtual environment: {venv_path}")
        
        # Check if we're actually in the venv
        if sys.prefix == sys.base_prefix:
            issues.append("⚠️  Virtual environment exists but not activated")
        else:
            print(f"   ✅ Virtual environment active: {sys.prefix}")
    else:
        issues.append(f"❌ Virtual environment missing: {venv_path}")
    
    # Check key modules
    modules_to_check = [
        'PyQt6', 'numpy', 'pyvisa', 'pyqtgraph'
    ]
    
    for module in modules_to_check:
        try:
            __import__(module)
            print(f"   ✅ Module {module}: Available")
        except ImportError:
            issues.append(f"❌ Module {module}: Missing")
    
    # Check project structure
    key_paths = [
        'dp2031_gui',
        'dp2031_gui/app.py',
        'dp2031_gui/core',
        'dp2031_gui/ui',
        'tests',
        'requirements.txt'
    ]
    
    for path in key_paths:
        full_path = project_root / path
        if full_path.exists():
            print(f"   ✅ Path {path}: Found")
        else:
            issues.append(f"❌ Path {path}: Missing")
    
    # Check log directory
    log_dir = project_root / "logs"
    if log_dir.exists():
        print(f"   ✅ Log directory: {log_dir}")
        log_files = list(log_dir.glob("*.log"))
        print(f"   📝 Log files: {len(log_files)} found")
    else:
        print(f"   ⚠️  Log directory will be created: {log_dir}")
    
    if issues:
        print("\n⚠️  ISSUES FOUND:")
        for issue in issues:
            print(f"      {issue}")
        print("\n💡 SOLUTIONS:")
        print("   1. Run: setup_venv.bat")
        print("   2. Activate venv: .venv\\Scripts\\activate")
        print("   3. Install deps: pip install -r requirements.txt")
        return False
    else:
        print("   ✅ All checks passed!")
        return True

def debug_main():
    """Main debug entry point with enhanced error handling."""
    
    debug_banner()
    
    # Enhanced environment check
    if not check_debug_environment():
        print("\n❌ Environment issues detected. Please fix before debugging.")
        return 1
    
    print("\n🚀 STARTING DEBUG SESSION...")
    print("-" * 70)
    
    try:
        # Import with detailed error info
        try:
            from dp2031_gui.app import main as app_main
            print("✅ Successfully imported dp2031_gui.app")
        except ImportError as e:
            print(f"❌ Import failed: {e}")
            print("📍 Traceback:")
            traceback.print_exc()
            return 1
        
        # Prepare debug arguments
        debug_args = ['--debug', '--log-level', 'DEBUG']
        
        # Add additional debug flags based on command line
        if '--verbose' in sys.argv:
            print("🔊 Verbose mode enabled")
        
        if '--mock' in sys.argv:
            print("🎭 Mock hardware mode enabled")
            debug_args.append('--demo')
        
        if '--profile' in sys.argv:
            print("⏱️  Performance profiling enabled")
            # Could add profiling here
        
        # Override sys.argv for the application
        original_argv = sys.argv.copy()
        sys.argv = [sys.argv[0]] + debug_args
        
        print(f"🎯 Debug args passed to app: {debug_args}")
        print("\n" + "=" * 70)
        
        # Run the application
        start_time = time.time()
        result = app_main()
        end_time = time.time()
        
        print("\n" + "=" * 70)
        print("🏁 DEBUG SESSION COMPLETED")
        print(f"⏱️  Runtime: {end_time - start_time:.2f} seconds")
        print(f"🔢 Exit code: {result}")
        
        # Restore original argv
        sys.argv = original_argv
        
        return result
        
    except KeyboardInterrupt:
        print("\n⏹️  Debug session interrupted by user")
        return 0
        
    except Exception as e:
        print(f"\n❌ CRITICAL DEBUG ERROR: {e}")
        print("\n📍 FULL TRACEBACK:")
        traceback.print_exc()
        
        print("\n🔍 DEBUG INFORMATION:")
        print(f"   Python version: {sys.version}")
        print(f"   Working directory: {os.getcwd()}")
        print(f"   Python path: {sys.path[:3]}...")
        print(f"   Environment: {os.environ.get('VIRTUAL_ENV', 'Not in venv')}")
        
        return 1

def show_debug_help():
    """Show debug-specific help."""
    
    help_text = """
🐛 DP2031 Debug Mode - Usage Guide

DEBUG OPTIONS:
    python debug.py                  # Full debug mode
    python debug.py --verbose        # Extra verbose output  
    python debug.py --mock           # Mock hardware mode
    python debug.py --profile        # Performance profiling
    python debug.py --help           # This help
    
DEBUG FEATURES:
    ✅ Enhanced error reporting
    ✅ Detailed environment checking
    ✅ Full logging to console & file
    ✅ Performance timing
    ✅ Import troubleshooting
    ✅ Traceback analysis
    
TROUBLESHOOTING TOOLS:
    python debug.py --check          # Environment check only
    python -c "import dp2031_gui"    # Test imports
    python -m pytest tests/ -v      # Run tests verbosely
    
LOG LOCATIONS:
    logs/dp2031_app.log             # Application log
    logs/dp2031_errors.log          # Error log  
    logs/dp2031_scpi.log            # SCPI communication
    logs/dp2031_data_*.csv          # Measurement data
    
COMMON ISSUES:
    • Virtual environment not activated
    • Missing dependencies (run setup_venv.bat)
    • VISA driver not installed (warning only)
    • PyQt6 display issues (check display drivers)
    
For production use: python main.py
"""
    print(help_text)

if __name__ == "__main__":
    
    # Handle help request
    if "--help" in sys.argv or "-h" in sys.argv:
        show_debug_help()
        sys.exit(0)
    
    # Handle check-only mode
    if "--check" in sys.argv:
        debug_banner()
        success = check_debug_environment()
        sys.exit(0 if success else 1)
    
    # Run debug session
    try:
        exit_code = debug_main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⏹️  Debug session terminated. Goodbye!")
        sys.exit(0)
