"""
Main entry point for DP2031 Industrial Power Controller.

This module allows the application to be run as a Python module:
    python -m dp2031_gui

It imports and executes the main application from app.py.
"""

import sys
from .app import main

if __name__ == "__main__":
    sys.exit(main())
