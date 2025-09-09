#!/usr/bin/env python3
"""
Test script for ConnectionDialog
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication
from dp2031_gui.ui.widgets import ConnectionDialog

def test_connection_dialog():
    """Test the ConnectionDialog standalone."""
    
    app = QApplication(sys.argv)
    
    # Create and show dialog
    dialog = ConnectionDialog()
    
    def on_connection_requested(resource):
        print(f"Connection requested to: {resource}")
        dialog.accept()
    
    dialog.connection_requested.connect(on_connection_requested)
    
    # Show dialog
    result = dialog.exec()
    
    if result == dialog.DialogCode.Accepted:
        print("Dialog accepted")
    else:
        print("Dialog cancelled")
    
    app.quit()

if __name__ == "__main__":
    test_connection_dialog()
