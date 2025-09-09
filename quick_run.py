#!/usr/bin/env python3
"""
DP2031 Industrial Power Controller - Quick Run

Minimal entry point for quick testing and demonstration.
Starts the application with minimal logging and fastest startup.

Usage:
    python quick_run.py              # Quick start with minimal logging
    python quick_run.py --silent     # Silent mode (errors only)
    python quick_run.py --demo       # Demo mode with simulated hardware

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

def quick_start():
    """Quick start with minimal output."""
    
    print("🚀 DP2031 Quick Start")
    print("-" * 30)
    
    try:
        # Quick environment check
        if not (project_root / "dp2031_gui").exists():
            print("❌ dp2031_gui package not found!")
            return 1
        
        # Import and run
        from dp2031_gui.app import main as app_main
        
        # Set minimal logging
        if "--silent" in sys.argv:
            os.environ['DP2031_LOG_LEVEL'] = 'ERROR'
            print("🔇 Silent mode (errors only)")
        else:
            os.environ['DP2031_LOG_LEVEL'] = 'WARNING'
            print("⚡ Minimal logging mode")
        
        # Demo mode
        if "--demo" in sys.argv:
            sys.argv.append('--demo')
            print("🎭 Demo mode enabled")
        
        print("✅ Starting application...")
        
        # Run the application
        return app_main()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Try: python debug.py --check")
        return 1
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 For detailed debugging: python debug.py")
        return 1

if __name__ == "__main__":
    
    if "--help" in sys.argv:
        print("""
🚀 DP2031 Quick Run - Usage

OPTIONS:
    python quick_run.py              # Quick start
    python quick_run.py --silent     # Silent mode  
    python quick_run.py --demo       # Demo mode
    python quick_run.py --help       # This help

For full features: python main.py
For debugging: python debug.py
        """)
        sys.exit(0)
    
    try:
        exit_code = quick_start()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⏹️  Stopped")
        sys.exit(0)
