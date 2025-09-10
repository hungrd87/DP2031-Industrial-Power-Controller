#!/usr/bin/env python3
"""
Debug script to check actual border colors being used
"""

import sys
from reusable_theme_system.theme_manager import ThemeManager, get_industrial_lcd_stylesheet

def debug_border_colors():
    """Debug and print actual border colors"""
    manager = ThemeManager()
    
    print("=== THEME COLORS DEBUG ===")
    
    # Light theme
    print("\n🔆 LIGHT THEME:")
    light_colors = manager.get_theme_colors("light")
    print(f"  border: {light_colors.get('border', 'NOT FOUND')}")
    print(f"  surface: {light_colors.get('surface', 'NOT FOUND')}")
    print(f"  primary: {light_colors.get('primary', 'NOT FOUND')}")
    
    # Dark theme  
    print("\n🌙 DARK THEME:")
    dark_colors = manager.get_theme_colors("dark")
    print(f"  border: {dark_colors.get('border', 'NOT FOUND')}")
    print(f"  surface: {dark_colors.get('surface', 'NOT FOUND')}")
    print(f"  primary: {dark_colors.get('primary', 'NOT FOUND')}")
    
    # LCD Stylesheets
    print("\n📺 LCD STYLESHEETS:")
    
    print("\n🔆 Light LCD Stylesheet:")
    light_lcd = get_industrial_lcd_stylesheet("light")
    print(light_lcd[:500] + "...")  # First 500 chars
    
    print("\n🌙 Dark LCD Stylesheet:")
    dark_lcd = get_industrial_lcd_stylesheet("dark")
    print(dark_lcd[:500] + "...")  # First 500 chars

if __name__ == "__main__":
    debug_border_colors()
