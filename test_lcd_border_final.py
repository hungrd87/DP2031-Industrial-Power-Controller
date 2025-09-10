#!/usr/bin/env python3
"""
Test để kiểm tra border color của QLCDNumber với các theme khác nhau
"""

import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLCDNumber, QPushButton)
from PyQt6.QtCore import Qt

# Add project path for imports
sys.path.append('.')

from reusable_theme_system.theme_manager import get_industrial_lcd_stylesheet

class LCDBorderTestWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.current_theme = 'dark'
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('QLCDNumber Border Color Test')
        self.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout()
        
        # Theme toggle button
        self.theme_btn = QPushButton(f'Current: {self.current_theme.title()} Theme (Click to Toggle)')
        self.theme_btn.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_btn)
        
        # LCD Number
        self.lcd_number = QLCDNumber()
        self.lcd_number.setDigitCount(8)
        self.lcd_number.display('123.45')
        self.lcd_number.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)
        layout.addWidget(self.lcd_number)
        
        # Units label
        self.units_label = QLabel('Volts (V)')
        self.units_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.units_label)
        
        # Border info
        self.border_info = QLabel()
        self.border_info.setWordWrap(True)
        layout.addWidget(self.border_info)
        
        # Instructions
        instructions = QLabel('''
<b>Border Test Instructions:</b><br>
• Check if border is visible and well-contrasted<br>
• Dark theme should have lighter border (#30363d)<br> 
• Light theme should have standard border (#e9ecef)<br>
• Toggle theme to compare both modes
        ''')
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        self.setLayout(layout)
        self.apply_theme()
        
    def toggle_theme(self):
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        self.theme_btn.setText(f'Current: {self.current_theme.title()} Theme (Click to Toggle)')
        self.apply_theme()
        
    def apply_theme(self):
        # Apply theme to QLCDNumber
        lcd_stylesheet = get_industrial_lcd_stylesheet(self.current_theme)
        self.lcd_number.setStyleSheet(lcd_stylesheet)
        
        # Update border info
        border_color = '#30363d' if self.current_theme == 'dark' else '#e9ecef'
        bg_color = '#0a0a0a' if self.current_theme == 'dark' else '#1a1a1a'
        
        self.border_info.setText(f"""
<b>Current Theme:</b> {self.current_theme.title()}<br>
<b>LCD Background:</b> {bg_color}<br>
<b>Border Color:</b> {border_color}<br>
<b>Expected:</b> Border should be clearly visible against the LCD background
        """)
        
        # Update window background
        if self.current_theme == 'dark':
            self.setStyleSheet("""
                QWidget { 
                    background-color: #0d1117; 
                    color: #f0f6fc; 
                }
                QLabel { 
                    color: #f0f6fc; 
                }
                QPushButton { 
                    background-color: #21262d; 
                    color: #f0f6fc; 
                    border: 1px solid #30363d;
                    padding: 8px;
                    border-radius: 4px;
                }
                QPushButton:hover { 
                    background-color: #30363d; 
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget { 
                    background-color: #ffffff; 
                    color: #24292f; 
                }
                QLabel { 
                    color: #24292f; 
                }
                QPushButton { 
                    background-color: #f6f8fa; 
                    color: #24292f; 
                    border: 1px solid #d0d7de;
                    padding: 8px;
                    border-radius: 4px;
                }
                QPushButton:hover { 
                    background-color: #f3f4f6; 
                }
            """)

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    widget = LCDBorderTestWidget()
    widget.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
