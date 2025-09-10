#!/usr/bin/env python3
"""
Test theme consistency from fresh start
"""

import sys
from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QApplication

def reset_settings():
    """Clear all settings for fresh test"""
    settings = QSettings('RIGOL', 'DP2031_Controller')
    settings.clear()
    settings.sync()
    print("✅ All settings cleared")

def set_theme(theme_name):
    """Set specific theme"""
    settings = QSettings('RIGOL', 'DP2031_Controller')
    settings.setValue("theme", theme_name)
    settings.sync()
    print(f"✅ Theme set to: {theme_name}")

def check_theme():
    """Check current theme"""
    settings = QSettings('RIGOL', 'DP2031_Controller')
    theme = settings.value("theme", "NOT_SET")
    print(f"📋 Current saved theme: {theme}")
    return theme

def main():
    app = QApplication(sys.argv)
    
    print("=== THEME CONSISTENCY TEST ===\n")
    
    print("1. Checking current state:")
    check_theme()
    
    print("\n2. Clearing all settings:")
    reset_settings()
    check_theme()
    
    print("\n3. Setting dark theme:")
    set_theme("dark")
    check_theme()
    
    print("\n✅ Test completed. App should now start with dark theme consistently.")
    
    print("\n💡 Next steps:")
    print("   - Run: python -m dp2031_gui")
    print("   - Verify: Dark theme loads from start")
    print("   - Test: Theme switching works correctly")

if __name__ == '__main__':
    main()
