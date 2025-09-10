#!/usr/bin/env python3
"""
Test script to measure button size directly in main application
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from dp2031_gui.ui.main_window import MainWindow

class MainAppButtonTest:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = None
        
    def start_test(self):
        """Start the main application and measure button size."""
        print("🚀 Starting main application for button measurement...")
        
        # Create main window
        self.main_window = MainWindow()
        self.main_window.show()
        
        # Timer to measure after window is fully loaded
        timer = QTimer()
        timer.timeout.connect(self.measure_buttons)
        timer.setSingleShot(True)
        timer.start(2000)  # Wait 2 seconds for full loading
        
        print("⏳ Waiting 2 seconds for application to fully load...")
        
        try:
            sys.exit(self.app.exec())
        except KeyboardInterrupt:
            print("\n✋ Test interrupted by user")
            sys.exit(0)
    
    def measure_buttons(self):
        """Measure all output buttons in the main window."""
        print("\n" + "="*60)
        print("🔍 MEASURING OUTPUT BUTTONS IN MAIN APPLICATION")
        print("="*60)
        
        # Get channel tabs widget
        channel_tabs = self.main_window.channel_tabs
        
        for i in range(channel_tabs.count()):
            tab_widget = channel_tabs.widget(i)
            tab_name = channel_tabs.tabText(i)
            
            print(f"\n📋 {tab_name}:")
            print("-" * 30)
            
            # Find the ChannelControlWidget
            channel_control = None
            for child in tab_widget.findChildren(type(tab_widget)):
                if hasattr(child, 'output_btn'):
                    channel_control = child
                    break
            
            if not channel_control:
                # Look deeper in the widget hierarchy
                for child in tab_widget.findChildren(object):
                    if hasattr(child, 'output_btn'):
                        channel_control = child
                        break
            
            if channel_control and hasattr(channel_control, 'output_btn'):
                btn = channel_control.output_btn
                
                # Force update
                btn.updateGeometry()
                
                # Get measurements
                min_width = btn.minimumWidth()
                max_width = btn.maximumWidth()
                actual_width = btn.width()
                actual_height = btn.height()
                geometry = btn.geometry()
                size_hint = btn.sizeHint()
                
                print(f"   📏 Width Constraints:")
                print(f"      Minimum: {min_width}px")
                print(f"      Maximum: {max_width}px")
                print(f"      Actual:  {actual_width}px")
                print(f"   📐 Height: {actual_height}px")
                print(f"   📍 Position: ({geometry.x()}, {geometry.y()})")
                print(f"   💡 Size Hint: {size_hint.width()} x {size_hint.height()}")
                print(f"   🔤 Text: '{btn.text()}'")
                
                # Check if it matches our expectations
                if min_width == 0 and max_width == 16777215:
                    print("   ✅ Width constraints are FREE (as expected)")
                else:
                    print(f"   ⚠️  Width constraints are NOT free!")
                    print(f"      Expected: min=0, max=16777215")
                    print(f"      Actual: min={min_width}, max={max_width}")
                    
            else:
                print("   ❌ Could not find output button in this tab!")
        
        print("\n" + "="*60)
        print("📊 SUMMARY")
        print("="*60)
        print("If width constraints show min=0, max=16777215, then buttons are FREE")
        print("If width constraints show other values, there may be cached/old constraints")
        print("\n💡 Press Ctrl+C to exit the test")

def main():
    print("Main Application Button Size Test")
    print("=" * 40)
    print("This will start the main application and measure")
    print("the actual button sizes in the running program.")
    print()
    
    test = MainAppButtonTest()
    test.start_test()

if __name__ == "__main__":
    main()
