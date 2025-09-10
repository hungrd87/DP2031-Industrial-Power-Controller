#!/usr/bin/env python3
"""
Side-by-side comparison of original BigDigitDisplay vs new QLCDNumber implementation
This shows the main app with both display types for comparison
"""

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLCDNumber, QGroupBox, 
                             QPushButton, QSplitter)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
import random

# Import our custom components
from dp2031_gui.ui.widgets import BigDigitDisplay
from reusable_theme_system.theme_manager import apply_theme_to_application, get_industrial_lcd_stylesheet

class DisplayComparisonMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DP2031 Display Comparison: BigDigitDisplay vs QLCDNumber")
        self.setGeometry(50, 50, 1400, 800)
        
        self.current_theme = "dark"
        
        # Test values
        self.test_values = {
            1: {'voltage': 12.345, 'current': 2.678, 'power': 33.123},
            2: {'voltage': 5.000, 'current': 1.200, 'power': 6.000},
            3: {'voltage': 24.750, 'current': 0.850, 'power': 21.038}
        }
        
        self.setup_ui()
        self.setup_timer()
        
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("DP2031 Channel Status Display Comparison")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Controls
        theme_btn = QPushButton("Toggle Theme")
        theme_btn.clicked.connect(self.toggle_theme)
        header_layout.addWidget(theme_btn)
        
        self.auto_btn = QPushButton("Start Simulation")
        self.auto_btn.clicked.connect(self.toggle_simulation)
        header_layout.addWidget(self.auto_btn)
        
        main_layout.addLayout(header_layout)
        
        # Comparison panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left: Original BigDigitDisplay
        left_panel = self.create_original_panel()
        splitter.addWidget(left_panel)
        
        # Right: New QLCDNumber
        right_panel = self.create_new_panel()
        splitter.addWidget(right_panel)
        
        splitter.setSizes([700, 700])
        
        # Status area
        status_layout = QHBoxLayout()
        
        # Original status
        self.original_status = QLabel("Original Implementation: BigDigitDisplay - Custom industrial widgets")
        self.original_status.setFont(QFont("Arial", 10))
        status_layout.addWidget(self.original_status)
        
        # New status
        self.new_status = QLabel("New Implementation: QLCDNumber - Standard Qt LCD widgets")
        self.new_status.setFont(QFont("Arial", 10))
        status_layout.addWidget(self.new_status)
        
        main_layout.addLayout(status_layout)
        
        self.update_all_displays()
        
    def create_original_panel(self):
        """Create panel with original BigDigitDisplay implementation"""
        panel = QGroupBox("ORIGINAL: BigDigitDisplay Implementation")
        panel.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout = QVBoxLayout(panel)
        
        # Quick status layout
        quick_status_layout = QHBoxLayout()
        
        # Create widgets similar to main app
        self.original_widgets = {}
        for channel in [1, 2, 3]:
            channel_frame = QGroupBox(f"Channel {channel}")
            channel_frame.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            channel_layout = QVBoxLayout(channel_frame)
            
            # Create BigDigitDisplay widgets
            voltage_display = BigDigitDisplay("Voltage", "V", precision=3, compact=True)
            current_display = BigDigitDisplay("Current", "A", precision=3, compact=True)
            power_display = BigDigitDisplay("Power", "W", precision=2, compact=True)
            
            channel_layout.addWidget(voltage_display)
            channel_layout.addWidget(current_display)
            channel_layout.addWidget(power_display)
            
            self.original_widgets[channel] = {
                'voltage': voltage_display,
                'current': current_display,
                'power': power_display
            }
            
            quick_status_layout.addWidget(channel_frame)
        
        layout.addLayout(quick_status_layout)
        
        # Total power (original style)
        total_layout = QHBoxLayout()
        total_layout.addStretch()
        self.original_total = BigDigitDisplay("Total Power", "W", precision=2)
        total_layout.addWidget(self.original_total)
        total_layout.addStretch()
        layout.addLayout(total_layout)
        
        return panel
        
    def create_new_panel(self):
        """Create panel with new QLCDNumber implementation"""
        panel = QGroupBox("NEW: QLCDNumber Implementation")
        panel.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout = QVBoxLayout(panel)
        
        # Quick status layout
        quick_status_layout = QHBoxLayout()
        
        # Create widgets similar to updated main app
        self.new_widgets = {}
        for channel in [1, 2, 3]:
            channel_frame = QGroupBox(f"Channel {channel}")
            channel_frame.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            channel_layout = QVBoxLayout(channel_frame)
            
            # Create LCD display widgets
            voltage_display = self.create_lcd_display("Voltage", "V", precision=3, compact=True)
            current_display = self.create_lcd_display("Current", "A", precision=3, compact=True)
            power_display = self.create_lcd_display("Power", "W", precision=2, compact=True)
            
            channel_layout.addWidget(voltage_display['container'])
            channel_layout.addWidget(current_display['container'])
            channel_layout.addWidget(power_display['container'])
            
            self.new_widgets[channel] = {
                'voltage': voltage_display,
                'current': current_display,
                'power': power_display
            }
            
            quick_status_layout.addWidget(channel_frame)
        
        layout.addLayout(quick_status_layout)
        
        # Total power (new style)
        total_layout = QHBoxLayout()
        total_layout.addStretch()
        self.new_total = self.create_lcd_display("Total Power", "W", precision=2)
        total_layout.addWidget(self.new_total['container'])
        total_layout.addStretch()
        layout.addLayout(total_layout)
        
        return panel
        
    def create_lcd_display(self, label: str, unit: str, precision: int = 3, compact: bool = False) -> dict:
        """Create LCD display widget with label and unit (same as main app)."""
        container = QWidget()
        container.setObjectName("lcd_container")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)
        
        # Label
        if label:
            label_widget = QLabel(label)
            label_widget.setObjectName("lcd_label")
            font = QFont("Arial", 8 if compact else 10, QFont.Weight.Bold)
            label_widget.setFont(font)
            label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label_widget)
        
        # LCD Display with industrial styling
        lcd = QLCDNumber(6)  # 6 digits for xxx.xxx format
        lcd.setMode(QLCDNumber.Mode.Dec)
        lcd.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
        height = 40 if compact else 60
        lcd.setMinimumHeight(height)
        lcd.setMaximumHeight(height)
        
        # Apply industrial LCD stylesheet
        lcd_style = get_industrial_lcd_stylesheet(self.current_theme)
        lcd.setStyleSheet(lcd_style)
        
        layout.addWidget(lcd)
        
        # Unit
        if unit:
            unit_widget = QLabel(unit)
            unit_widget.setObjectName("lcd_unit")
            font = QFont("Arial", 8 if compact else 10, QFont.Weight.Bold)
            unit_widget.setFont(font)
            unit_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(unit_widget)
        
        # Apply container styling
        container.setStyleSheet(lcd_style)
        
        return {
            'container': container,
            'lcd': lcd,
            'precision': precision,
            'set_value': lambda value: lcd.display(f"{value:.{precision}f}")
        }
        
    def setup_timer(self):
        """Setup simulation timer"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.simulate_data)
        self.simulating = False
        
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        apply_theme_to_application(QApplication.instance(), self.current_theme)
        
    def toggle_simulation(self):
        """Toggle data simulation"""
        if self.simulating:
            self.timer.stop()
            self.auto_btn.setText("Start Simulation")
            self.simulating = False
        else:
            self.timer.start(750)  # Update every 750ms
            self.auto_btn.setText("Stop Simulation")
            self.simulating = True
            
    def simulate_data(self):
        """Simulate changing power supply data"""
        for channel in [1, 2, 3]:
            # Add small random variations
            self.test_values[channel]['voltage'] += random.uniform(-0.05, 0.05)
            self.test_values[channel]['current'] += random.uniform(-0.02, 0.02)
            
            # Keep within bounds
            self.test_values[channel]['voltage'] = max(0, min(30, self.test_values[channel]['voltage']))
            self.test_values[channel]['current'] = max(0, min(5, self.test_values[channel]['current']))
            self.test_values[channel]['power'] = (self.test_values[channel]['voltage'] * 
                                                  self.test_values[channel]['current'])
        
        self.update_all_displays()
        
    def update_all_displays(self):
        """Update all display widgets with current values"""
        total_power = 0
        
        for channel in [1, 2, 3]:
            values = self.test_values[channel]
            
            # Update original widgets (BigDigitDisplay)
            self.original_widgets[channel]['voltage'].set_value(values['voltage'])
            self.original_widgets[channel]['current'].set_value(values['current'])
            self.original_widgets[channel]['power'].set_value(values['power'])
            
            # Update new widgets (QLCDNumber)
            self.new_widgets[channel]['voltage']['set_value'](values['voltage'])
            self.new_widgets[channel]['current']['set_value'](values['current'])
            self.new_widgets[channel]['power']['set_value'](values['power'])
            
            total_power += values['power']
        
        # Update total power displays
        self.original_total.set_value(total_power)
        self.new_total['set_value'](total_power)


def main():
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("DP2031 Display Comparison")
    app.setApplicationVersion("1.0")
    
    # Apply initial theme
    apply_theme_to_application(app, "dark")
    
    window = DisplayComparisonMainWindow()
    window.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
