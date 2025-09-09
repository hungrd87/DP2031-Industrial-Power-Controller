"""
PyQt6 Professional Theme System - Reusable Package
==================================================

A complete theming system for PyQt6 applications with professional design standards.
Supports light and dark themes with consistent styling across all Qt controls.

Features:
- Light and Dark professional themes
- Desktop-standard sizing (24px heights, consistent widths)
- Complete text color consistency
- Interactive states (hover/pressed/checked)
- SVG icons for modern appearance
- ScrollArea and all controls styling
- Easy integration with any PyQt6 project

Author: RTB2000 Project Team
License: MIT
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "RTB2000 Project Team"
__license__ = "MIT"

from .theme_manager import ThemeManager, get_theme_stylesheet, apply_theme_to_application, get_available_themes
from .theme_constants import LIGHT_THEME_COLORS, DARK_THEME_COLORS, COMMON_SIZES

__all__ = [
    'ThemeManager',
    'get_theme_stylesheet', 
    'apply_theme_to_application',
    'get_available_themes',
    'LIGHT_THEME_COLORS',
    'DARK_THEME_COLORS', 
    'COMMON_SIZES'
]
