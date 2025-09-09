#!/usr/bin/env python3
"""
Test Connect Action with Mock Resource
=====================================

Test script to verify Connect action behavior with a simulated device connection.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer
from dp2031_gui.ui.main_window import MainWindow

def test_connect_action():
    """Test Connect action with manual verification."""
    
    app = QApplication(sys.argv)
    
    # Create main window
    window = MainWindow()
    
    # Simulate having a last resource
    window.last_resource = "TCPIP::192.168.1.100::INSTR"
    print(f"✓ Set mock last resource: {window.last_resource}")
    
    # Show window
    window.show()
    
    # Instructions for manual testing
    instructions = """
Connect Action Test Instructions:
=================================

1. Click Connect action in toolbar
2. Should see log: "Attempting to connect to last resource: TCPIP::192.168.1.100::INSTR"
3. Connection will fail (no real device) but action should uncheck automatically
4. Click Connect again - should show same behavior (attempt direct connection)

Check the console output for connection attempt logs.
"""
    
    QMessageBox.information(window, "Test Instructions", instructions)
    
    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    test_connect_action()
