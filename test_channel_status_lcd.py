#!/usr/bin/env python3
"""
Test to integrate QLCDNumber into existing Channel Status for comparison
This creates a modified version of the quick status panel with both display types
"""

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLCDNumber, QGroupBox, 
                             QPushButton, QTabWidget, QTextEdit, QSplitter)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
import random

# Import our custom components
from dp2031_gui.ui.widgets import BigDigitDisplay
from reusable_theme_system.theme_manager import apply_theme_to_application

class ChannelStatusTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Channel Status: BigDigitDisplay vs QLCDNumber Test")
        self.setGeometry(100, 100, 1200, 700)
        
        self.current_theme = "dark"
        
        self.setup_ui()
        self.setup_timer()
        
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # Header with controls
        header_layout = QHBoxLayout()
        
        title = QLabel("Channel Status Display Comparison")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Theme toggle
        theme_btn = QPushButton("Toggle Theme")
        theme_btn.clicked.connect(self.toggle_theme)
        header_layout.addWidget(theme_btn)
        
        # Auto update toggle
        self.auto_btn = QPushButton("Start Auto Update")
        self.auto_btn.clicked.connect(self.toggle_auto_update)
        header_layout.addWidget(self.auto_btn)
        
        main_layout.addLayout(header_layout)
        
        # Create tabs similar to main application
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Channel Status tab with both display types
        self.create_channel_status_tab()
        
        # Initialize values
        self.voltage_value = 12.345
        self.current_value = 2.678
        self.power_value = 33.123
        
        self.update_displays()
        
    def create_channel_status_tab(self):
        """Create Channel Status tab with both display types"""
        status_widget = QWidget()
        layout = QVBoxLayout(status_widget)
        
        # Create splitter for side-by-side comparison
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)
        
        # Left side: Current BigDigitDisplay implementation
        left_panel = self.create_big_digit_panel()
        splitter.addWidget(left_panel)
        
        # Right side: QLCDNumber alternative
        right_panel = self.create_lcd_panel()
        splitter.addWidget(right_panel)
        
        # Set equal sizes
        splitter.setSizes([600, 600])
        
        # Add log area
        log_group = QGroupBox("Comparison Notes")
        log_layout = QVBoxLayout(log_group)
        
        self.log_area = QTextEdit()
        self.log_area.setMaximumHeight(150)
        self.log_area.append("BigDigitDisplay Features:")
        self.log_area.append("• Custom labels and units integrated")
        self.log_area.append("• Professional industrial styling")
        self.log_area.append("• Theme-aware colors")
        self.log_area.append("• Configurable precision")
        self.log_area.append("• Compact mode support")
        self.log_area.append("")
        self.log_area.append("QLCDNumber Features:")
        self.log_area.append("• Classic LCD/LED appearance")
        self.log_area.append("• Built-in Qt widget (stable)")
        self.log_area.append("• Multiple segment styles")
        self.log_area.append("• Numeric display only")
        self.log_area.append("• Separate unit labels needed")
        
        log_layout.addWidget(self.log_area)
        layout.addWidget(log_group)
        
        self.tab_widget.addTab(status_widget, "Channel Status Comparison")
        
    def create_big_digit_panel(self):
        """Create panel with BigDigitDisplay widgets (current implementation)"""
        panel = QGroupBox("Current Implementation: BigDigitDisplay")
        panel.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout = QVBoxLayout(panel)
        
        # Status header
        status_header = QLabel("Channel Status - Output Measurements")
        status_header.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        status_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(status_header)
        
        # Measurements layout
        measurements_layout = QHBoxLayout()
        
        # Voltage
        self.big_voltage = BigDigitDisplay(label="Voltage", unit="V", precision=3)
        measurements_layout.addWidget(self.big_voltage)
        
        # Current
        self.big_current = BigDigitDisplay(label="Current", unit="A", precision=3)
        measurements_layout.addWidget(self.big_current)
        
        # Power
        self.big_power = BigDigitDisplay(label="Power", unit="W", precision=3)
        measurements_layout.addWidget(self.big_power)
        
        layout.addLayout(measurements_layout)
        
        # Additional info
        info_layout = QVBoxLayout()
        self.big_status_label = QLabel("Status: Normal Operation")
        self.big_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(self.big_status_label)
        
        layout.addLayout(info_layout)
        
        return panel
        
    def create_lcd_panel(self):
        """Create panel with QLCDNumber widgets (alternative)"""
        panel = QGroupBox("Alternative: QLCDNumber")
        panel.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout = QVBoxLayout(panel)
        
        # Status header
        status_header = QLabel("Channel Status - Output Measurements")
        status_header.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        status_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(status_header)
        
        # Measurements layout
        measurements_layout = QHBoxLayout()
        
        # Voltage
        voltage_group = QVBoxLayout()
        voltage_label = QLabel("Voltage")
        voltage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        voltage_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        voltage_group.addWidget(voltage_label)
        
        self.lcd_voltage = QLCDNumber(6)
        self.lcd_voltage.setMode(QLCDNumber.Mode.Dec)
        self.lcd_voltage.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
        self.lcd_voltage.setMinimumHeight(60)
        voltage_group.addWidget(self.lcd_voltage)
        
        voltage_unit = QLabel("V")
        voltage_unit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        voltage_unit.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        voltage_group.addWidget(voltage_unit)
        
        measurements_layout.addLayout(voltage_group)
        
        # Current
        current_group = QVBoxLayout()
        current_label = QLabel("Current")
        current_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        current_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        current_group.addWidget(current_label)
        
        self.lcd_current = QLCDNumber(6)
        self.lcd_current.setMode(QLCDNumber.Mode.Dec)
        self.lcd_current.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
        self.lcd_current.setMinimumHeight(60)
        current_group.addWidget(self.lcd_current)
        
        current_unit = QLabel("A")
        current_unit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        current_unit.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        current_group.addWidget(current_unit)
        
        measurements_layout.addLayout(current_group)
        
        # Power
        power_group = QVBoxLayout()
        power_label = QLabel("Power")
        power_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        power_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        power_group.addWidget(power_label)
        
        self.lcd_power = QLCDNumber(6)
        self.lcd_power.setMode(QLCDNumber.Mode.Dec)
        self.lcd_power.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
        self.lcd_power.setMinimumHeight(60)
        power_group.addWidget(self.lcd_power)
        
        power_unit = QLabel("W")
        power_unit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        power_unit.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        power_group.addWidget(power_unit)
        
        measurements_layout.addLayout(power_group)
        
        layout.addLayout(measurements_layout)
        
        # Additional info
        info_layout = QVBoxLayout()
        self.lcd_status_label = QLabel("Status: Normal Operation")
        self.lcd_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(self.lcd_status_label)
        
        layout.addLayout(info_layout)
        
        return panel
        
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
            self.auto_btn.setText("Start Auto Update")
            self.auto_updating = False
        else:
            self.timer.start(800)  # Update every 800ms
            self.auto_btn.setText("Stop Auto Update")
            self.auto_updating = True
            
    def auto_update(self):
        """Automatically update values with random variations"""
        # Simulate power supply readings with realistic variations
        self.voltage_value += random.uniform(-0.05, 0.05)
        self.current_value += random.uniform(-0.02, 0.02)
        
        # Keep within bounds
        self.voltage_value = max(0, min(30, self.voltage_value))
        self.current_value = max(0, min(5, self.current_value))
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
    app.setApplicationName("Channel Status Display Test")
    app.setApplicationVersion("1.0")
    
    # Apply initial theme
    apply_theme_to_application(app, "dark")
    
    window = ChannelStatusTestWindow()
    window.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
