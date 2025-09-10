#!/usr/bin/env python3
"""
Debug script to inspect actual button properties in running application
"""

import sys
import time
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import QTimer, QObject, pyqtSignal
from dp2031_gui.ui.main_window import MainWindow
from dp2031_gui.core.model import PowerSupplyModel

class ButtonDebugger(QObject):
    finished = pyqtSignal()
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        
    def debug_buttons(self):
        """Debug all output buttons in the application."""
        print("\n" + "="*60)
        print("🐛 DEBUGGING OUTPUT BUTTONS IN RUNNING APPLICATION")
        print("="*60)
        
        try:
            # Get the central widget (QTabWidget)
            central_widget = self.main_window.centralWidget()
            print(f"📱 Central widget type: {type(central_widget)}")
            
            if hasattr(central_widget, 'count'):
                tab_count = central_widget.count()
                print(f"📋 Found {tab_count} tabs")
                
                for i in range(tab_count):
                    tab_widget = central_widget.widget(i)
                    tab_text = central_widget.tabText(i)
                    print(f"\n📂 Tab {i}: '{tab_text}'")
                    print(f"   Widget type: {type(tab_widget)}")
                    
                    # Find all widgets recursively
                    self.find_output_buttons(tab_widget, tab_text, level=1)
            else:
                print("❌ Central widget is not a tab widget!")
                # Search in central widget directly
                self.find_output_buttons(central_widget, "Central", level=0)
                
        except Exception as e:
            print(f"❌ Error during debug: {e}")
            import traceback
            traceback.print_exc()
        
        self.finished.emit()
    
    def find_output_buttons(self, widget, context, level=0):
        """Recursively find output buttons."""
        indent = "  " * level
        
        # Check if this widget has output_btn
        if hasattr(widget, 'output_btn'):
            btn = widget.output_btn
            print(f"{indent}🎯 FOUND OUTPUT BUTTON in {context}!")
            print(f"{indent}   Widget type: {type(widget)}")
            print(f"{indent}   Button type: {type(btn)}")
            
            # Get detailed measurements
            min_w = btn.minimumWidth()
            max_w = btn.maximumWidth()
            actual_w = btn.width()
            actual_h = btn.height()
            size_hint = btn.sizeHint()
            geometry = btn.geometry()
            
            print(f"{indent}   📏 Width constraints:")
            print(f"{indent}      Minimum: {min_w}px")
            print(f"{indent}      Maximum: {max_w}px")
            print(f"{indent}      Actual: {actual_w}px")
            print(f"{indent}   📐 Height: {actual_h}px")
            print(f"{indent}   💡 Size hint: {size_hint.width()}x{size_hint.height()}px")
            print(f"{indent}   📍 Geometry: {geometry.x()},{geometry.y()} {geometry.width()}x{geometry.height()}")
            print(f"{indent}   🔤 Text: '{btn.text()}'")
            print(f"{indent}   ✨ Checkable: {btn.isCheckable()}")
            print(f"{indent}   🎨 Enabled: {btn.isEnabled()}")
            print(f"{indent}   👁️ Visible: {btn.isVisible()}")
            
            # Check stylesheet
            stylesheet = btn.styleSheet()
            if stylesheet:
                print(f"{indent}   🎨 Has custom stylesheet: {len(stylesheet)} chars")
                if "width" in stylesheet.lower():
                    print(f"{indent}   ⚠️  Stylesheet contains 'width'!")
            else:
                print(f"{indent}   🎨 No custom stylesheet")
                
            # Check if constraints are what we expect
            if min_w == 0 and max_w >= 16777000:
                print(f"{indent}   ✅ Width is FREE (as expected)")
            else:
                print(f"{indent}   ❌ Width has CONSTRAINTS!")
                
            return True
        
        # Search children
        found_any = False
        if hasattr(widget, 'children'):
            children = widget.children()
            for child in children:
                if isinstance(child, QWidget):
                    if self.find_output_buttons(child, f"{context}>child", level + 1):
                        found_any = True
        
        return found_any

def main():
    print("🚀 Starting Application Debug Mode")
    print("This will start the full application and debug button properties")
    
    # Create application
    app = QApplication(sys.argv)
    
    # Create model and main window
    main_window = MainWindow()
    main_window.show()
    
    print("⏳ Application started, waiting 3 seconds for full initialization...")
    
    # Create debugger
    debugger = ButtonDebugger(main_window)
    
    # Timer to start debugging after app is ready
    timer = QTimer()
    timer.timeout.connect(debugger.debug_buttons)
    timer.setSingleShot(True)
    timer.start(3000)  # Wait 3 seconds
    
    # Connect finished signal to quit
    debugger.finished.connect(lambda: (
        print("\n🎯 Debug completed! Check the output above."),
        print("💡 Press Ctrl+C to exit the application."),
        app.quit()
    ))
    
    print("📱 Main window displayed. Debug will start in 3 seconds...")
    
    try:
        sys.exit(app.exec())
    except KeyboardInterrupt:
        print("\n👋 Debug session ended.")
        sys.exit(0)

if __name__ == "__main__":
    main()
