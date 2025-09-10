#!/usr/bin/env python3
"""
Test script to compare BigDigitDisplay vs QLCDNumber for Channel Status values
This script shows both display types side by side for comparison
"""

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLCDNumber, QGroupBox, 
                             QPushButton, QSlider)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
import random

# Import our custom BigDigitDisplay
from dp2031_gui.ui.widgets import BigDigitDisplay
from reusable_theme_system.theme_manager import apply_theme_to_application

class DisplayComparisonWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BigDigitDisplay vs QLCDNumber - Comparison Test")
        self.setGeometry(100, 100, 1000, 600)
        
        # Initialize theme
        self.current_theme = "dark"
        
        self.setup_ui()
        self.setup_timer()
        
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("Display Widget Comparison: BigDigitDisplay vs QLCDNumber")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Theme toggle button
        theme_btn = QPushButton("Toggle Theme (Dark/Light)")
        theme_btn.clicked.connect(self.toggle_theme)
        main_layout.addWidget(theme_btn)
        
        # Comparison layout
        comparison_layout = QHBoxLayout()
        main_layout.addLayout(comparison_layout)
        
        # BigDigitDisplay Group
        self.setup_big_digit_group(comparison_layout)
        
        # QLCDNumber Group
        self.setup_lcd_group(comparison_layout)
        
        # Control panel
        self.setup_controls(main_layout)
        
        # Current values
        self.voltage_value = 12.345
        self.current_value = 2.678
        self.power_value = 33.123
        
        self.update_displays()
        
    def setup_big_digit_group(self, parent_layout):
        """Setup BigDigitDisplay widgets group"""
        group = QGroupBox("BigDigitDisplay (Current Implementation)")
        group.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout = QVBoxLayout(group)
        
        # Voltage
        layout.addWidget(QLabel("Voltage:"))
        self.big_voltage = BigDigitDisplay(label="Output Voltage", unit="V", precision=3)
        layout.addWidget(self.big_voltage)
        
        # Current
        layout.addWidget(QLabel("Current:"))
        self.big_current = BigDigitDisplay(label="Output Current", unit="A", precision=3)
        layout.addWidget(self.big_current)
        
        # Power
        layout.addWidget(QLabel("Power:"))
        self.big_power = BigDigitDisplay(label="Output Power", unit="W", precision=3)
        layout.addWidget(self.big_power)
        
        parent_layout.addWidget(group)
        
    def setup_lcd_group(self, parent_layout):
        """Setup QLCDNumber widgets group"""
        group = QGroupBox("QLCDNumber (Alternative)")
        group.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout = QVBoxLayout(group)
        
        # Voltage
        layout.addWidget(QLabel("Voltage:"))
        voltage_layout = QVBoxLayout()
        self.lcd_voltage = QLCDNumber(6)  # 6 digits for xxx.xxx
        self.lcd_voltage.setMode(QLCDNumber.Mode.Dec)
        self.lcd_voltage.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
        voltage_layout.addWidget(self.lcd_voltage)
        voltage_unit = QLabel("V")
        voltage_unit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        voltage_layout.addWidget(voltage_unit)
        layout.addLayout(voltage_layout)
        
        # Current
        layout.addWidget(QLabel("Current:"))
        current_layout = QVBoxLayout()
        self.lcd_current = QLCDNumber(6)
        self.lcd_current.setMode(QLCDNumber.Mode.Dec)
        self.lcd_current.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
        current_layout.addWidget(self.lcd_current)
        current_unit = QLabel("A")
        current_unit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        current_layout.addWidget(current_unit)
        layout.addLayout(current_layout)
        
        # Power
        layout.addWidget(QLabel("Power:"))
        power_layout = QVBoxLayout()
        self.lcd_power = QLCDNumber(6)
        self.lcd_power.setMode(QLCDNumber.Mode.Dec)
        self.lcd_power.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
        power_layout.addWidget(self.lcd_power)
        power_unit = QLabel("W")
        power_unit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        power_layout.addWidget(power_unit)
        layout.addLayout(power_layout)
        
        parent_layout.addWidget(group)
        
    def setup_controls(self, parent_layout):
        """Setup control panel"""
        controls_group = QGroupBox("Simulation Controls")
        controls_layout = QVBoxLayout(controls_group)
        
        # Auto update toggle
        self.auto_btn = QPushButton("Start Auto Update (Simulated Data)")
        self.auto_btn.clicked.connect(self.toggle_auto_update)
        controls_layout.addWidget(self.auto_btn)
        
        # Manual sliders
        sliders_layout = QHBoxLayout()
        
        # Voltage slider
        v_layout = QVBoxLayout()
        v_layout.addWidget(QLabel("Voltage (0-30V)"))
        self.voltage_slider = QSlider(Qt.Orientation.Horizontal)
        self.voltage_slider.setRange(0, 300)  # 0-30.0V (x10)
        self.voltage_slider.setValue(123)  # 12.3V
        self.voltage_slider.valueChanged.connect(self.manual_update)
        v_layout.addWidget(self.voltage_slider)
        sliders_layout.addLayout(v_layout)
        
        # Current slider
        i_layout = QVBoxLayout()
        i_layout.addWidget(QLabel("Current (0-5A)"))
        self.current_slider = QSlider(Qt.Orientation.Horizontal)
        self.current_slider.setRange(0, 500)  # 0-5.0A (x100)
        self.current_slider.setValue(267)  # 2.67A
        self.current_slider.valueChanged.connect(self.manual_update)
        i_layout.addWidget(self.current_slider)
        sliders_layout.addLayout(i_layout)
        
        controls_layout.addLayout(sliders_layout)
        parent_layout.addWidget(controls_group)
        
    def setup_timer(self):
        """Setup timer for auto updates"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.auto_update)
        self.auto_updating = False
        
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        apply_theme_to_application(QApplication.instance(), self.current_theme)
        
    def toggle_auto_update(self):
        """Toggle automatic value updates"""
        if self.auto_updating:
            self.timer.stop()
            self.auto_btn.setText("Start Auto Update (Simulated Data)")
            self.auto_updating = False
        else:
            self.timer.start(500)  # Update every 500ms
            self.auto_btn.setText("Stop Auto Update")
            self.auto_updating = True
            
    def auto_update(self):
        """Automatically update values with random variations"""
        # Simulate small variations in power supply readings
        self.voltage_value += random.uniform(-0.1, 0.1)
        self.current_value += random.uniform(-0.05, 0.05)
        
        # Keep within reasonable bounds
        self.voltage_value = max(0, min(30, self.voltage_value))
        self.current_value = max(0, min(5, self.current_value))
        self.power_value = self.voltage_value * self.current_value
        
        self.update_displays()
        
    def manual_update(self):
        """Update values from sliders"""
        if not self.auto_updating:
            self.voltage_value = self.voltage_slider.value() / 10.0
            self.current_value = self.current_slider.value() / 100.0
            self.power_value = self.voltage_value * self.current_value
            self.update_displays()
        
    def update_displays(self):
        """Update all display widgets"""
        # BigDigitDisplay widgets
        self.big_voltage.set_value(self.voltage_value)
        self.big_current.set_value(self.current_value)
        self.big_power.set_value(self.power_value)
        
        # QLCDNumber widgets
        self.lcd_voltage.display(f"{self.voltage_value:.3f}")
        self.lcd_current.display(f"{self.current_value:.3f}")
        self.lcd_power.display(f"{self.power_value:.3f}")


def main():
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Display Comparison Test")
    app.setApplicationVersion("1.0")
    
    # Apply initial theme
    apply_theme_to_application(app, "dark")
    
    window = DisplayComparisonWindow()
    window.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
