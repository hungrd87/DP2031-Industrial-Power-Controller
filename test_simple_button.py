#!/usr/bin/env python3
"""
Simple test to verify current button implementation
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from dp2031_gui.ui.widgets import ChannelControlWidget

def test_current_button():
    """Test the current button implementation."""
    app = QApplication(sys.argv)
    
    print("🔍 Testing Current Button Implementation")
    print("=" * 50)
    
    # Create widget
    widget = ChannelControlWidget(1)
    btn = widget.output_btn
    
    # Show widget to trigger layout
    window = QMainWindow()
    window.setCentralWidget(widget)
    window.show()
    
    # Process events to ensure layout is complete
    app.processEvents()
    
    # Get current state
    min_width = btn.minimumWidth()
    max_width = btn.maximumWidth()
    actual_width = btn.width()
    size_hint = btn.sizeHint()
    
    print(f"📏 Button Width Analysis:")
    print(f"   Minimum Width: {min_width}px")
    print(f"   Maximum Width: {max_width}px")
    print(f"   Actual Width:  {actual_width}px")
    print(f"   Size Hint Width: {size_hint.width()}px")
    print()
    
    # Check source code to verify our changes
    import inspect
    source_lines = inspect.getsource(ChannelControlWidget._setup_ui)
    
    print("📝 Source Code Check:")
    if "setMinimumWidth" in source_lines:
        print("   ⚠️  Found setMinimumWidth in source!")
        for i, line in enumerate(source_lines.split('\n')):
            if 'setMinimumWidth' in line:
                print(f"   Line {i+1}: {line.strip()}")
    else:
        print("   ✅ No setMinimumWidth found in source")
        
    if "setMaximumWidth" in source_lines:
        print("   ⚠️  Found setMaximumWidth in source!")
        for i, line in enumerate(source_lines.split('\n')):
            if 'setMaximumWidth' in line:
                print(f"   Line {i+1}: {line.strip()}")
    else:
        print("   ✅ No setMaximumWidth found in source")
    
    # Expected vs actual
    print(f"\n📊 Analysis:")
    if min_width == 0 and max_width >= 16777000:  # Allow some variance
        print("   ✅ Button width is FREE as expected")
    else:
        print("   ❌ Button width still has constraints!")
        print(f"      Expected: min=0, max≈16777215")
        print(f"      Actual: min={min_width}, max={max_width}")
    
    print(f"\n💡 The button text '{btn.text()}' fits in {actual_width}px")
    
    app.quit()

if __name__ == "__main__":
    test_current_button()
