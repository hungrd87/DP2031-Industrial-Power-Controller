#!/usr/bin/env python3
"""
Test to compare border colors between BigDigitDisplay and QLCDNumber
"""

import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLCDNumber, QPushButton)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Add project path for imports
sys.path.append('.')

from reusable_theme_system.theme_manager import get_industrial_lcd_stylesheet
from dp2031_gui.ui.widgets import BigDigitDisplay

class BorderComparisonWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.current_theme = 'dark'
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Border Color Comparison')
        self.setGeometry(100, 100, 800, 600)
        
        layout = QVBoxLayout()
        
        # Theme toggle button
        self.theme_btn = QPushButton(f'Current: {self.current_theme.title()} Theme (Click to Toggle)')
        self.theme_btn.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_btn)
        
        # Main content
        content_layout = QHBoxLayout()
        
        # BigDigitDisplay side
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel('<h3>BigDigitDisplay</h3>'))
        
        self.big_digit = BigDigitDisplay()
        self.big_digit.set_value(123.45, "V")
        left_layout.addWidget(self.big_digit)
        
        content_layout.addLayout(left_layout)
        
        # QLCDNumber side  
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel('<h3>QLCDNumber</h3>'))
        
        self.lcd_number = QLCDNumber()
        self.lcd_number.setDigitCount(8)
        self.lcd_number.display('123.45')
        self.lcd_number.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)
        right_layout.addWidget(self.lcd_number)
        
        # Add units label
        self.units_label = QLabel('V')
        self.units_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(self.units_label)
        
        content_layout.addLayout(right_layout)
        
        layout.addLayout(content_layout)
        
        # Instructions
        instructions = QLabel('''
<b>Border Comparison:</b><br>
• Both widgets should have similar border appearance<br>
• Dark theme: lighter border on dark background<br>
• Light theme: standard border on light background<br>
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
        # Apply theme to BigDigitDisplay
        self.big_digit.set_theme(self.current_theme)
        
        # Apply theme to QLCDNumber
        lcd_stylesheet = get_industrial_lcd_stylesheet(self.current_theme)
        self.lcd_number.setStyleSheet(lcd_stylesheet)
        
        # Update background
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
    
    widget = BorderComparisonWidget()
    widget.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
