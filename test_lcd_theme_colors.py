#!/usr/bin/env python3
"""
Test to verify theme color changes in main application LCD widgets
"""

import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLCDNumber, QPushButton, QTextEdit)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

# Add project path for imports
sys.path.append('.')

from reusable_theme_system.theme_manager import get_industrial_lcd_stylesheet

class ThemeTestWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.current_theme = 'dark'
        self.init_ui()
        
        # Auto-toggle timer for demo
        self.timer = QTimer()
        self.timer.timeout.connect(self.auto_toggle)
        
    def init_ui(self):
        self.setWindowTitle('LCD Theme Color Test')
        self.setGeometry(100, 100, 700, 500)
        
        layout = QVBoxLayout()
        
        # Controls
        controls_layout = QHBoxLayout()
        
        self.theme_btn = QPushButton(f'Theme: {self.current_theme.title()} (Click to Toggle)')
        self.theme_btn.clicked.connect(self.toggle_theme)
        controls_layout.addWidget(self.theme_btn)
        
        self.auto_btn = QPushButton('Start Auto-Toggle (3s)')
        self.auto_btn.clicked.connect(self.toggle_auto)
        controls_layout.addWidget(self.auto_btn)
        
        layout.addLayout(controls_layout)
        
        # LCD Display
        self.lcd = QLCDNumber()
        self.lcd.setDigitCount(8)
        self.lcd.display('123.456')
        self.lcd.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
        self.lcd.setMinimumHeight(80)
        layout.addWidget(self.lcd)
        
        # Current colors display
        self.color_info = QTextEdit()
        self.color_info.setMaximumHeight(150)
        self.color_info.setReadOnly(True)
        layout.addWidget(self.color_info)
        
        # Instructions
        instructions = QLabel('''
<h3>Theme Color Test Instructions:</h3>
<b>Expected Behavior:</b><br>
• <b>Dark Theme:</b> Dark background (#0a0a0a), cyan digits (#00ccff), light border (#30363d)<br>
• <b>Light Theme:</b> Dark background (#1a1a1a), green digits (#00ff41), light border (#e9ecef)<br><br>
<b>What to Check:</b><br>
• Both digit color AND border color should change when toggling theme<br>
• Numbers should be clearly visible in both themes<br>
• Border should be visible and contrasting
        ''')
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        self.setLayout(layout)
        self.apply_theme()
        
    def toggle_theme(self):
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        self.theme_btn.setText(f'Theme: {self.current_theme.title()} (Click to Toggle)')
        self.apply_theme()
        
    def toggle_auto(self):
        if self.timer.isActive():
            self.timer.stop()
            self.auto_btn.setText('Start Auto-Toggle (3s)')
        else:
            self.timer.start(3000)  # 3 seconds
            self.auto_btn.setText('Stop Auto-Toggle')
            
    def auto_toggle(self):
        self.toggle_theme()
        
    def apply_theme(self):
        # Get LCD stylesheet
        lcd_stylesheet = get_industrial_lcd_stylesheet(self.current_theme)
        self.lcd.setStyleSheet(lcd_stylesheet)
        
        # Show current colors in text area
        if self.current_theme == 'dark':
            colors_text = """DARK THEME COLORS:
Background: #0a0a0a (very dark)
Digit Color: #00ccff (cyan/blue) 
Border: #30363d (light gray)
Expected: Cyan digits on dark background with visible border"""
        else:
            colors_text = """LIGHT THEME COLORS:
Background: #1a1a1a (dark)
Digit Color: #00ff41 (green)
Border: #e9ecef (light gray)
Expected: Green digits on dark background with visible border"""
            
        self.color_info.setPlainText(colors_text)
        
        # Update window background to match theme
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
                QTextEdit {
                    background-color: #21262d;
                    color: #f0f6fc;
                    border: 1px solid #30363d;
                    padding: 4px;
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
                QTextEdit {
                    background-color: #f6f8fa;
                    color: #24292f;
                    border: 1px solid #d0d7de;
                    padding: 4px;
                }
            """)

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    widget = ThemeTestWidget()
    widget.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
