#!/usr/bin/env python3
"""
Test script to verify output button width changes
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from dp2031_gui.ui.widgets import ChannelControlWidget

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Output Button Width Test")
        self.setGeometry(100, 100, 400, 300)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Add info label
        info_label = QLabel("Testing Output Button Width - Should be 100-160px")
        layout.addWidget(info_label)
        
        # Create channel control widget
        self.channel_widget = ChannelControlWidget(1)
        layout.addWidget(self.channel_widget)
        
        # Check and print actual button dimensions
        self.check_button_size()
        
    def check_button_size(self):
        """Check and print button size constraints."""
        btn = self.channel_widget.output_btn
        min_width = btn.minimumWidth()
        max_width = btn.maximumWidth()
        actual_width = btn.width()
        
        print(f"🔍 Button Size Check:")
        print(f"   Min Width: {min_width}px")
        print(f"   Max Width: {max_width}px")
        print(f"   Actual Width: {actual_width}px")
        
        if min_width == 100 and max_width == 160:
            print("✅ Width constraints are correct (100-160px)")
        else:
            print("❌ Width constraints are wrong!")
            print(f"   Expected: min=100, max=160")
            print(f"   Actual: min={min_width}, max={max_width}")

def main():
    app = QApplication(sys.argv)
    
    print("Output Button Width Test")
    print("=" * 30)
    
    window = TestWindow()
    window.show()
    
    # Force update to get actual size
    app.processEvents()
    window.check_button_size()
    
    print("\nTest window is displayed. Check button visually.")
    print("Press Ctrl+C to exit.")
    
    try:
        sys.exit(app.exec())
    except KeyboardInterrupt:
        print("\nTest completed.")
        sys.exit(0)

if __name__ == "__main__":
    main()
