#!/usr/bin/env python3
"""
Test các cải tiến UI: button width, theme toolbar, label colors
"""

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLCDNumber, QPushButton, QToolBar, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QFont, QActionGroup

# Add project path for imports
sys.path.append('.')

from reusable_theme_system.theme_manager import get_industrial_lcd_stylesheet

class UITestWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_theme = 'dark'
        self.lcd_widgets = []
        self.lcd_label_widgets = []
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('UI Improvements Test')
        self.setGeometry(100, 100, 800, 600)
        
        # Create toolbar
        toolbar = self.addToolBar("Theme")
        
        # Theme actions
        theme_group = QActionGroup(self)
        
        self.dark_action = QAction("🌙 Dark", self)
        self.dark_action.setToolTip("Switch to dark theme")
        self.dark_action.setCheckable(True)
        self.dark_action.setChecked(True)
        self.dark_action.triggered.connect(lambda: self.set_theme("dark"))
        theme_group.addAction(self.dark_action)
        toolbar.addAction(self.dark_action)
        
        self.light_action = QAction("☀️ Light", self)
        self.light_action.setToolTip("Switch to light theme")
        self.light_action.setCheckable(True)
        self.light_action.triggered.connect(lambda: self.set_theme("light"))
        theme_group.addAction(self.light_action)
        toolbar.addAction(self.light_action)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # LCD displays with labels
        lcd_layout = QHBoxLayout()
        
        for label_text in ['V', 'A', 'W']:
            lcd_display = self.create_lcd_display(label_text)
            lcd_layout.addWidget(lcd_display['container'])
            
        layout.addLayout(lcd_layout)
        
        # Output buttons with width constraints
        button_layout = QHBoxLayout()
        
        for i in range(3):
            btn = QPushButton("OFF")
            btn.setCheckable(True)
            btn.setMinimumWidth(50)   # Test width constraints
            btn.setMaximumWidth(80)   # Test width constraints
            btn.setMinimumHeight(28)
            btn.setMaximumHeight(28)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #666666;
                    color: white;
                    font-weight: bold;
                    font-size: 12px;
                    border: 1px solid #888888;
                    border-radius: 4px;
                }
                QPushButton:checked {
                    background-color: #00aa00;
                    border-color: #00cc00;
                    text: "ON";
                }
                QPushButton:hover {
                    border-color: #aaaaaa;
                }
            """)
            button_layout.addWidget(btn)
            
        layout.addLayout(button_layout)
        
        # Test info
        info = QLabel('''
<h3>UI Improvements Test</h3>
<b>✅ Features to Test:</b><br>
• <b>Toolbar Theme Switcher:</b> Click 🌙/☀️ buttons in toolbar<br>
• <b>Label Color Updates:</b> V, A, W labels should change color with theme<br>
• <b>Button Width Limits:</b> Output buttons have min=50px, max=80px width<br>
• <b>LCD Theme Updates:</b> LCD numbers should change color with theme
        ''')
        info.setWordWrap(True)
        layout.addWidget(info)
        
        self.apply_theme()
        
    def create_lcd_display(self, label):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)
        
        # Label
        label_widget = QLabel(label)
        label_widget.setObjectName("lcd_label")
        font = QFont("Arial", 10, QFont.Weight.Bold)
        label_widget.setFont(font)
        label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label_widget)
        self.lcd_label_widgets.append(label_widget)
        
        # LCD
        lcd = QLCDNumber(6)
        lcd.setMode(QLCDNumber.Mode.Dec)
        lcd.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
        lcd.setMinimumHeight(60)
        lcd.setMaximumHeight(60)
        lcd.display("123.45")
        layout.addWidget(lcd)
        self.lcd_widgets.append(lcd)
        
        return {'container': container, 'lcd': lcd}
        
    def set_theme(self, theme_name):
        self.current_theme = theme_name
        
        # Update action states
        self.dark_action.setChecked(theme_name == "dark")
        self.light_action.setChecked(theme_name == "light")
        
        self.apply_theme()
        
    def apply_theme(self):
        # Update LCD widgets
        lcd_style = get_industrial_lcd_stylesheet(self.current_theme)
        for lcd_widget in self.lcd_widgets:
            lcd_widget.setStyleSheet(lcd_style)
            
        # Update labels
        label_color = "#f0f6fc" if self.current_theme == "dark" else "#24292f"
        for label_widget in self.lcd_label_widgets:
            label_widget.setStyleSheet(f"""
                QLabel {{
                    color: {label_color};
                    font-weight: bold;
                    background-color: transparent;
                    border: none;
                }}
            """)
            
        # Update window background
        if self.current_theme == 'dark':
            self.setStyleSheet("""
                QMainWindow { 
                    background-color: #0d1117; 
                    color: #f0f6fc; 
                }
                QWidget { 
                    background-color: #0d1117; 
                    color: #f0f6fc; 
                }
                QLabel { 
                    color: #f0f6fc; 
                }
                QToolBar {
                    background-color: #21262d;
                    border: 1px solid #30363d;
                }
                QToolBar QToolButton {
                    background-color: #21262d;
                    color: #f0f6fc;
                    border: 1px solid #30363d;
                    padding: 4px 8px;
                    margin: 2px;
                    border-radius: 4px;
                }
                QToolBar QToolButton:checked {
                    background-color: #1f6feb;
                    border-color: #58a6ff;
                }
                QToolBar QToolButton:hover {
                    background-color: #30363d;
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow { 
                    background-color: #ffffff; 
                    color: #24292f; 
                }
                QWidget { 
                    background-color: #ffffff; 
                    color: #24292f; 
                }
                QLabel { 
                    color: #24292f; 
                }
                QToolBar {
                    background-color: #f6f8fa;
                    border: 1px solid #d0d7de;
                }
                QToolBar QToolButton {
                    background-color: #f6f8fa;
                    color: #24292f;
                    border: 1px solid #d0d7de;
                    padding: 4px 8px;
                    margin: 2px;
                    border-radius: 4px;
                }
                QToolBar QToolButton:checked {
                    background-color: #0969da;
                    color: white;
                    border-color: #0550ae;
                }
                QToolBar QToolButton:hover {
                    background-color: #f3f4f6;
                }
            """)

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    widget = UITestWidget()
    widget.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
