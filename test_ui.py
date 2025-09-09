#!/usr/bin/env python3
"""
Simple test launcher for DP2031 UI components.

This script tests the UI components independently to ensure they work correctly.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import Qt
except ImportError:
    print("ERROR: PyQt6 not found. Please install with: pip install PyQt6")
    sys.exit(1)

def test_ui_components():
    """Test UI components individually."""
    
    app = QApplication(sys.argv)
    app.setApplicationName("DP2031 UI Test")
    
    try:
        # Test imports
        print("Testing UI component imports...")
        
        from dp2031_gui.ui.widgets import (
            BigDigitDisplay, StatusLamp, ConnectionWidget,
            ChannelControlWidget, StatusWidget, TrendWidget, AlarmWidget
        )
        print("✓ Widget imports successful")
        
        from dp2031_gui.ui.main_window import MainWindow
        print("✓ MainWindow import successful")
        
        from dp2031_gui.ui import apply_industrial_theme
        print("✓ Theme import successful")
        
        # Apply theme
        apply_industrial_theme(app)
        print("✓ Industrial theme applied")
        
        # Test basic widget creation
        print("\nTesting widget creation...")
        
        # Test BigDigitDisplay
        display = BigDigitDisplay("Test", "V", precision=3)
        display.set_value(5.123)
        print("✓ BigDigitDisplay created")
        
        # Test StatusLamp
        lamp = StatusLamp("Test Status")
        lamp.set_state(True)
        print("✓ StatusLamp created")
        
        # Test ConnectionWidget
        conn_widget = ConnectionWidget()
        print("✓ ConnectionWidget created")
        
        # Test ChannelControlWidget
        channel_widget = ChannelControlWidget(1)
        print("✓ ChannelControlWidget created")
        
        # Test StatusWidget
        status_widget = StatusWidget(1)
        print("✓ StatusWidget created")
        
        # Test TrendWidget
        trend_widget = TrendWidget()
        print("✓ TrendWidget created")
        
        # Test AlarmWidget
        alarm_widget = AlarmWidget()
        print("✓ AlarmWidget created")
        
        print("\n" + "="*50)
        print("All UI components tested successfully!")
        print("="*50)
        
        # Create and show main window briefly
        print("\nCreating main window...")
        main_window = MainWindow()
        main_window.show()
        print("✓ MainWindow created and shown")
        
        # Close after 2 seconds
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(2000, app.quit)
        
        return app.exec()
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    print("DP2031 UI Component Test")
    print("=" * 30)
    
    exit_code = test_ui_components()
    
    if exit_code == 0:
        print("\n🎉 All tests passed!")
    else:
        print("\n💥 Tests failed!")
    
    sys.exit(exit_code)
