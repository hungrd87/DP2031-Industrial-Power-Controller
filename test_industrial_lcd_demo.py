#!/usr/bin/env python3
"""
Simple demo showcasing industrial QLCDNumber styling
Shows different color schemes and segment styles
"""

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLCDNumber, QGroupBox, 
                             QPushButton, QComboBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
import random

from reusable_theme_system.theme_manager import apply_theme_to_application, get_industrial_lcd_stylesheet

class IndustrialLCDDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Industrial QLCDNumber Styling Demo")
        self.setGeometry(100, 100, 800, 600)
        
        self.current_theme = "dark"
        self.values = [12.345, 2.678, 33.123, 240.75]
        
        self.setup_ui()
        self.setup_timer()
        
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Industrial QLCDNumber Display Styling")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Controls
        theme_btn = QPushButton("Toggle Theme")
        theme_btn.clicked.connect(self.toggle_theme)
        header_layout.addWidget(theme_btn)
        
        segment_combo = QComboBox()
        segment_combo.addItems(["Filled", "Outline", "Flat"])
        segment_combo.currentTextChanged.connect(self.change_segment_style)
        header_layout.addWidget(segment_combo)
        
        self.sim_btn = QPushButton("Start Simulation")
        self.sim_btn.clicked.connect(self.toggle_simulation)
        header_layout.addWidget(self.sim_btn)
        
        layout.addLayout(header_layout)
        
        # LCD Display Groups
        displays_layout = QHBoxLayout()
        
        # Voltage
        voltage_group = self.create_lcd_group("Voltage", "V", self.values[0], precision=3)
        displays_layout.addWidget(voltage_group)
        
        # Current
        current_group = self.create_lcd_group("Current", "A", self.values[1], precision=3)
        displays_layout.addWidget(current_group)
        
        # Power
        power_group = self.create_lcd_group("Power", "W", self.values[2], precision=2)
        displays_layout.addWidget(power_group)
        
        # Frequency
        freq_group = self.create_lcd_group("Frequency", "Hz", self.values[3], precision=1)
        displays_layout.addWidget(freq_group)
        
        layout.addLayout(displays_layout)
        
        # Information
        info_text = QLabel("""
Industrial LCD Features:
• Dark background with colored border
• Bright digit colors for visibility
• Professional monospace font
• Theme-aware color schemes
• Hover effects for interactivity

Theme Colors:
- Dark Theme: Black background, blue border, cyan digits
- Light Theme: Dark background, white border, green digits
        """)
        info_text.setFont(QFont("Arial", 10))
        info_text.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(info_text)
        
        # Store LCD references
        self.lcds = [
            voltage_group.findChild(QLCDNumber),
            current_group.findChild(QLCDNumber),
            power_group.findChild(QLCDNumber),
            freq_group.findChild(QLCDNumber)
        ]
        
        self.update_displays()
        
    def create_lcd_group(self, label: str, unit: str, value: float, precision: int = 3) -> QGroupBox:
        """Create a group with industrial LCD display"""
        group = QGroupBox(f"{label} ({unit})")
        group.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout = QVBoxLayout(group)
        
        # Create LCD with industrial styling
        lcd = QLCDNumber(8)  # 8 digits for more space
        lcd.setMode(QLCDNumber.Mode.Dec)
        lcd.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
        lcd.setMinimumHeight(80)
        
        # Apply industrial styling
        lcd_style = get_industrial_lcd_stylesheet(self.current_theme)
        lcd.setStyleSheet(lcd_style)
        
        # Set initial value
        lcd.display(f"{value:.{precision}f}")
        
        layout.addWidget(lcd)
        
        return group
        
    def setup_timer(self):
        """Setup simulation timer"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.simulate_values)
        self.simulating = False
        
    def toggle_theme(self):
        """Toggle between dark and light themes"""
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        apply_theme_to_application(QApplication.instance(), self.current_theme)
        
        # Update LCD styling
        lcd_style = get_industrial_lcd_stylesheet(self.current_theme)
        for lcd in self.lcds:
            if lcd:
                lcd.setStyleSheet(lcd_style)
                
    def change_segment_style(self, style_name: str):
        """Change LCD segment style"""
        style_map = {
            "Filled": QLCDNumber.SegmentStyle.Filled,
            "Outline": QLCDNumber.SegmentStyle.Outline,
            "Flat": QLCDNumber.SegmentStyle.Flat
        }
        
        style = style_map.get(style_name, QLCDNumber.SegmentStyle.Filled)
        for lcd in self.lcds:
            if lcd:
                lcd.setSegmentStyle(style)
                
    def toggle_simulation(self):
        """Toggle value simulation"""
        if self.simulating:
            self.timer.stop()
            self.sim_btn.setText("Start Simulation")
            self.simulating = False
        else:
            self.timer.start(500)  # Update every 500ms
            self.sim_btn.setText("Stop Simulation")
            self.simulating = True
            
    def simulate_values(self):
        """Simulate changing values"""
        # Add random variations
        for i in range(len(self.values)):
            variation = random.uniform(-0.1, 0.1)
            self.values[i] += variation
            # Keep positive
            self.values[i] = max(0.001, self.values[i])
            
        self.update_displays()
        
    def update_displays(self):
        """Update all LCD displays"""
        precisions = [3, 3, 2, 1]  # voltage, current, power, frequency
        
        for i, (lcd, value, precision) in enumerate(zip(self.lcds, self.values, precisions)):
            if lcd:
                lcd.display(f"{value:.{precision}f}")


def main():
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Industrial LCD Demo")
    app.setApplicationVersion("1.0")
    
    # Apply initial theme
    apply_theme_to_application(app, "dark")
    
    window = IndustrialLCDDemo()
    window.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
