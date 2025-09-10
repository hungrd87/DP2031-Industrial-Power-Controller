#!/usr/bin/env python3
"""
Test script to measure actual output button size
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import QTimer
from dp2031_gui.ui.widgets import ChannelControlWidget

class ButtonSizeTest(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Actual Button Size Test")
        self.setGeometry(100, 100, 500, 400)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Add info label
        self.info_label = QLabel("Measuring actual button size...")
        layout.addWidget(self.info_label)
        
        # Create channel control widget
        self.channel_widget = ChannelControlWidget(1)
        layout.addWidget(self.channel_widget)
        
        # Timer to check size after widget is fully rendered
        self.timer = QTimer()
        self.timer.timeout.connect(self.measure_button_size)
        self.timer.setSingleShot(True)
        self.timer.start(500)  # Wait 500ms for full rendering
        
    def measure_button_size(self):
        """Measure and display actual button size."""
        btn = self.channel_widget.output_btn
        
        # Force layout update
        self.channel_widget.updateGeometry()
        btn.updateGeometry()
        
        # Get constraints
        min_width = btn.minimumWidth()
        max_width = btn.maximumWidth()
        min_height = btn.minimumHeight()
        max_height = btn.maximumHeight()
        
        # Get actual size
        actual_width = btn.width()
        actual_height = btn.height()
        
        # Get geometry info
        geometry = btn.geometry()
        size_hint = btn.sizeHint()
        
        print("=" * 50)
        print("🔍 BUTTON SIZE ANALYSIS")
        print("=" * 50)
        print(f"📏 Width Constraints:")
        print(f"   Minimum Width: {min_width}px")
        print(f"   Maximum Width: {max_width}px")
        print(f"   Actual Width:  {actual_width}px")
        print()
        print(f"📐 Height Constraints:")
        print(f"   Minimum Height: {min_height}px")
        print(f"   Maximum Height: {max_height}px")
        print(f"   Actual Height:  {actual_height}px")
        print()
        print(f"📍 Geometry:")
        print(f"   Position: ({geometry.x()}, {geometry.y()})")
        print(f"   Size: {geometry.width()} x {geometry.height()}")
        print()
        print(f"💡 Size Hint: {size_hint.width()} x {size_hint.height()}")
        print()
        
        # Verify if constraints are working
        if actual_width >= min_width and actual_width <= max_width:
            print("✅ Width is within constraints")
        else:
            print("❌ Width is NOT within constraints!")
            
        if actual_height >= min_height and actual_height <= max_height:
            print("✅ Height is within constraints")
        else:
            print("❌ Height is NOT within constraints!")
            
        # Update info label
        info_text = f"""
        <b>Button Size Measurement:</b><br>
        Width: {actual_width}px (min: {min_width}, max: {max_width})<br>
        Height: {actual_height}px (min: {min_height}, max: {max_height})<br>
        Position: ({geometry.x()}, {geometry.y()})<br>
        Size Hint: {size_hint.width()} x {size_hint.height()}
        """
        self.info_label.setText(info_text)
        
        # Check if button text fits
        text_width = btn.fontMetrics().horizontalAdvance(btn.text())
        print(f"🔤 Text Analysis:")
        print(f"   Button Text: '{btn.text()}'")
        print(f"   Text Width: {text_width}px")
        print(f"   Available Space: {actual_width}px")
        
        if text_width < actual_width:
            print("✅ Text fits in button")
        else:
            print("⚠️  Text might be cramped")

def main():
    app = QApplication(sys.argv)
    
    print("Starting Actual Button Size Test...")
    print("This will measure the real dimensions of the output button.")
    
    window = ButtonSizeTest()
    window.show()
    
    print("Window displayed. Measurement will start in 500ms...")
    print("Check console for detailed size analysis.")
    
    try:
        sys.exit(app.exec())
    except KeyboardInterrupt:
        print("\nTest completed.")
        sys.exit(0)

if __name__ == "__main__":
    main()
