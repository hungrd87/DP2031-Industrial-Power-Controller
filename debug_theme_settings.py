#!/usr/bin/env python3
"""
Debug script to check saved theme in QSettings
"""

import sys
from PyQt6.QtCore import QSettings

def main():
    # Check current saved theme
    settings = QSettings('RIGOL', 'DP2031_Controller')
    saved_theme = settings.value("theme", "DEFAULT_NOT_SET")
    
    print("=== THEME SETTINGS DEBUG ===")
    print(f"Saved theme: {saved_theme}")
    print(f"Theme type: {type(saved_theme)}")
    
    # Show all settings
    print("\n=== ALL SETTINGS ===")
    for key in settings.allKeys():
        value = settings.value(key)
        print(f"{key}: {value} ({type(value).__name__})")
    
    print("\n=== THEME CHANGE TEST ===")
    # Set theme to dark and verify
    settings.setValue("theme", "dark")
    settings.sync()
    verify_dark = settings.value("theme")
    print(f"After setting to 'dark': {verify_dark}")
    
    # Set theme to light and verify  
    settings.setValue("theme", "light")
    settings.sync()
    verify_light = settings.value("theme")
    print(f"After setting to 'light': {verify_light}")
    
    # Reset to original
    settings.setValue("theme", saved_theme if saved_theme != "DEFAULT_NOT_SET" else "dark")
    settings.sync()
    
    print(f"\nRestored original setting: {settings.value('theme')}")

if __name__ == '__main__':
    app = sys.modules.get('PyQt6.QtWidgets')
    if not app:
        from PyQt6.QtWidgets import QApplication
        app = QApplication(sys.argv)
    
    main()
