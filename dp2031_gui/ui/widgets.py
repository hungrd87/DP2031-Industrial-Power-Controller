"""
Industrial control widgets for DP2031 Power Controller.

Provides specialized widgets designed for industrial applications:
- Big digit displays for clear reading
- Status lamps with color coding
- Connection management widgets
- Channel control panels
- Trend plotting widgets
- Alarm management interfaces

All widgets follow industrial design principles with high contrast,
clear visual hierarchy, and robust operation.
"""

import sys
import time
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QLabel, QPushButton, QLineEdit, QDoubleSpinBox, QSpinBox,
    QCheckBox, QComboBox, QGroupBox, QFrame, QSlider, QProgressBar,
    QTableWidget, QTableWidgetItem, QTextEdit, QScrollArea,
    QSplitter, QTabWidget, QDialog, QDialogButtonBox, QMessageBox,
    QListWidget, QListWidgetItem, QHeaderView
)
from PyQt6.QtCore import (
    Qt, QTimer, pyqtSignal, QThread, QMutex, QSize, QRect
)
from PyQt6.QtGui import (
    QFont, QPalette, QColor, QPainter, QPen, QBrush, QPixmap,
    QFontMetrics, QLinearGradient
)

try:
    import pyqtgraph as pg
    PYQTGRAPH_AVAILABLE = True
except ImportError:
    PYQTGRAPH_AVAILABLE = False

from ..core.model import ChannelMeasurement, ProtectionSettings
from ..core.logging_cfg import get_logger


class BigDigitDisplay(QWidget):
    """
    Large digit display widget for industrial applications.
    
    Features:
    - Large, easily readable digits
    - Configurable precision
    - Unit display
    - Color coding for status
    - Compact mode for space-constrained areas
    """
    
    def __init__(self, label: str = "", unit: str = "", 
                 precision: int = 3, compact: bool = False):
        super().__init__()
        
        self.label = label
        self.unit = unit
        self.precision = precision
        self.compact = compact
        self.value = 0.0
        self.alarm_state = False
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the display widget."""
        layout = QVBoxLayout(self)
        layout.setSpacing(2)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Label
        if self.label:
            self.label_widget = QLabel(self.label)
            font = QFont("Arial", 8 if self.compact else 10, QFont.Weight.Bold)
            self.label_widget.setFont(font)
            self.label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # Label styling is now handled by theme manager
            layout.addWidget(self.label_widget)
        
        # Value display
        self.value_widget = QLabel("0.000")
        self.value_widget.setObjectName("industrial-value")  # For theme styling
        font_size = 14 if self.compact else 24
        font = QFont("Courier", font_size, QFont.Weight.Bold)
        self.value_widget.setFont(font)
        self.value_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Value widget styling is now handled by theme manager
        layout.addWidget(self.value_widget)
        
        # Unit display
        if self.unit:
            self.unit_widget = QLabel(self.unit)
            font = QFont("Arial", 8 if self.compact else 10, QFont.Weight.Bold)
            self.unit_widget.setFont(font)
            self.unit_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # Unit widget styling is now handled by theme manager
            layout.addWidget(self.unit_widget)
        
        # Set minimum size
        min_width = 80 if self.compact else 120
        min_height = 60 if self.compact else 100
        self.setMinimumSize(min_width, min_height)
    
    def set_value(self, value: float):
        """Set the displayed value."""
        self.value = value
        format_string = f"{{:.{self.precision}f}}"
        self.value_widget.setText(format_string.format(value))
        
        # Update color based on alarm state
        self._update_color()
    
    def set_alarm_state(self, alarm: bool):
        """Set alarm state (changes color)."""
        self.alarm_state = alarm
        self._update_color()
    
    def _update_color(self):
        """Update display color based on state."""
        if self.alarm_state:
            color = "#ff0000"  # Red for alarm
        else:
            color = "#00ff00"  # Green for normal
        
        self.value_widget.setStyleSheet(f"""
            QLabel {{
                background-color: #1a1a1a;
                border: 2px solid #666666;
                border-radius: 3px;
                padding: 5px;
                color: {color};
            }}
        """)


class StatusLamp(QWidget):
    """
    Industrial status lamp widget.
    
    Features:
    - Clear ON/OFF indication
    - Color coding (green/red/yellow)
    - Optional blinking for warnings
    - Text label
    """
    
    def __init__(self, label: str = ""):
        super().__init__()
        
        self.label = label
        self.state = False
        self.blink_state = False
        self.color_on = "#00ff00"   # Green
        self.color_off = "#333333"  # Dark gray
        
        self._setup_ui()
        
        # Blink timer
        self.blink_timer = QTimer()
        self.blink_timer.timeout.connect(self._toggle_blink)
    
    def _setup_ui(self):
        """Setup the lamp widget."""
        layout = QHBoxLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(2, 2, 2, 2)
        
        # Lamp circle
        self.lamp_widget = QLabel()
        self.lamp_widget.setFixedSize(20, 20)
        self.lamp_widget.setStyleSheet(f"""
            QLabel {{
                background-color: {self.color_off};
                border: 2px solid #666666;
                border-radius: 10px;
            }}
        """)
        layout.addWidget(self.lamp_widget)
        
        # Label
        if self.label:
            self.label_widget = QLabel(self.label)
            self.label_widget.setFont(QFont("Arial", 9))
            self.label_widget.setStyleSheet("color: #cccccc;")
            layout.addWidget(self.label_widget)
        
        # Set minimum size
        self.setMinimumSize(100, 25)
    
    def set_state(self, state: bool):
        """Set lamp state."""
        self.state = state
        self._update_display()
    
    def set_colors(self, on_color: str, off_color: str):
        """Set custom colors."""
        self.color_on = on_color
        self.color_off = off_color
        self._update_display()
    
    def set_blinking(self, blink: bool, interval: int = 500):
        """Enable/disable blinking."""
        if blink:
            self.blink_timer.start(interval)
        else:
            self.blink_timer.stop()
            self.blink_state = False
        self._update_display()
    
    def _toggle_blink(self):
        """Toggle blink state."""
        self.blink_state = not self.blink_state
        self._update_display()
    
    def _update_display(self):
        """Update lamp appearance."""
        if self.state and not self.blink_state:
            color = self.color_on
        else:
            color = self.color_off
        
        self.lamp_widget.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                border: 2px solid #666666;
                border-radius: 10px;
            }}
        """)


class ConnectionWidget(QWidget):
    """
    Connection management widget.
    
    Features:
    - Resource selection
    - Connection status
    - Auto-discovery
    - Connection parameters
    """
    
    connection_requested = pyqtSignal(str)
    disconnection_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        self.logger = get_logger('ConnectionWidget')
        self.available_resources = []
        
        self._setup_ui()
        self._refresh_resources()
    
    def _setup_ui(self):
        """Setup connection widget UI."""
        layout = QVBoxLayout(self)
        
        # Connection group
        connection_group = QGroupBox("Instrument Connection")
        connection_layout = QVBoxLayout(connection_group)
        
        # Resource selection
        resource_layout = QHBoxLayout()
        resource_layout.addWidget(QLabel("Resource:"))
        
        self.resource_combo = QComboBox()
        self.resource_combo.setEditable(True)
        resource_layout.addWidget(self.resource_combo)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self._refresh_resources)
        resource_layout.addWidget(refresh_btn)
        
        connection_layout.addLayout(resource_layout)
        
        # Connection buttons
        button_layout = QHBoxLayout()
        
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self._connect)
        self.connect_btn.setStyleSheet("""
            QPushButton {
                background-color: #00aa00;
                color: white;
                font-weight: bold;
                padding: 5px;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #00cc00;
            }
            QPushButton:disabled {
                background-color: #666666;
            }
        """)
        button_layout.addWidget(self.connect_btn)
        
        self.disconnect_btn = QPushButton("Disconnect")
        self.disconnect_btn.clicked.connect(self._disconnect)
        self.disconnect_btn.setEnabled(False)
        self.disconnect_btn.setStyleSheet("""
            QPushButton {
                background-color: #cc0000;
                color: white;
                font-weight: bold;
                padding: 5px;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #ff0000;
            }
            QPushButton:disabled {
                background-color: #666666;
            }
        """)
        button_layout.addWidget(self.disconnect_btn)
        
        connection_layout.addLayout(button_layout)
        
        # Status display
        self.status_label = QLabel("Disconnected")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #333333;
                border: 1px solid #666666;
                padding: 5px;
                border-radius: 3px;
                color: #cccccc;
            }
        """)
        connection_layout.addWidget(self.status_label)
        
        layout.addWidget(connection_group)
        
        # Connection parameters group
        params_group = QGroupBox("Connection Parameters")
        params_layout = QFormLayout(params_group)
        
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(1000, 30000)
        self.timeout_spin.setValue(5000)
        self.timeout_spin.setSuffix(" ms")
        params_layout.addRow("Timeout:", self.timeout_spin)
        
        self.auto_reconnect_check = QCheckBox("Auto-reconnect")
        self.auto_reconnect_check.setChecked(True)
        params_layout.addRow("", self.auto_reconnect_check)
        
        layout.addWidget(params_group)
        
        # Add stretch
        layout.addStretch()
    
    def _refresh_resources(self):
        """Refresh available VISA resources."""
        self.logger.info("Refreshing VISA resources")
        
        try:
            import pyvisa
            rm = pyvisa.ResourceManager()
            resources = rm.list_resources()
            
            self.resource_combo.clear()
            
            # Filter for likely DP2000/DP2031 resources
            dp_resources = []
            for resource in resources:
                if any(x in resource for x in ['USB', 'TCPIP', 'ASRL', 'GPIB']):
                    dp_resources.append(resource)
            
            self.resource_combo.addItems(dp_resources)
            
            # Add common manual entries
            manual_entries = [
                "USB0::0x1AB1::0x0E11::DP2D251800001::INSTR",
                "TCPIP0::192.168.1.100::INSTR",
                "ASRL3::INSTR",
                "GPIB0::7::INSTR"
            ]
            
            for entry in manual_entries:
                if entry not in dp_resources:
                    self.resource_combo.addItem(entry)
            
            self.available_resources = list(self.resource_combo.itemText(i) 
                                          for i in range(self.resource_combo.count()))
            
            self.logger.info(f"Found {len(self.available_resources)} resources")
            
        except Exception as e:
            self.logger.error(f"Error refreshing resources: {e}")
            QMessageBox.warning(self, "Resource Error", 
                              f"Failed to refresh VISA resources:\n{str(e)}")
    
    def _connect(self):
        """Request connection to selected resource."""
        resource = self.resource_combo.currentText().strip()
        if not resource:
            QMessageBox.warning(self, "Connection Error", "Please select a resource.")
            return
        
        self.logger.info(f"Requesting connection to: {resource}")
        self.connection_requested.emit(resource)
        
        # Update UI state
        self.connect_btn.setEnabled(False)
        self.disconnect_btn.setEnabled(True)
        self.status_label.setText("Connecting...")
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #aa6600;
                border: 1px solid #666666;
                padding: 5px;
                border-radius: 3px;
                color: white;
            }
        """)
    
    def _disconnect(self):
        """Request disconnection."""
        self.logger.info("Requesting disconnection")
        self.disconnection_requested.emit()
        
        # Update UI state
        self.connect_btn.setEnabled(True)
        self.disconnect_btn.setEnabled(False)
        self.status_label.setText("Disconnected")
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #333333;
                border: 1px solid #666666;
                padding: 5px;
                border-radius: 3px;
                color: #cccccc;
            }
        """)
    
    def update_connection_status(self, connected: bool, message: str = ""):
        """Update connection status display."""
        if connected:
            self.status_label.setText(f"Connected{': ' + message if message else ''}")
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: #00aa00;
                    border: 1px solid #666666;
                    padding: 5px;
                    border-radius: 3px;
                    color: white;
                }
            """)
        else:
            self.status_label.setText(f"Disconnected{': ' + message if message else ''}")
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: #cc0000;
                    border: 1px solid #666666;
                    padding: 5px;
                    border-radius: 3px;
                    color: white;
                }
            """)
            self.connect_btn.setEnabled(True)
            self.disconnect_btn.setEnabled(False)


class ChannelControlWidget(QWidget):
    """
    Channel control widget for voltage/current/protection settings.
    
    Features:
    - Voltage and current setpoints
    - Output enable/disable
    - Protection settings
    """
    
    settings_changed = pyqtSignal(int, dict)  # channel, settings
    output_toggled = pyqtSignal(int, bool)    # channel, state
    
    def __init__(self, channel: int):
        super().__init__()
        
        self.channel = channel
        self.logger = get_logger(f'ChannelControl_CH{channel}')
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup channel control UI with compact design."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)  # Further reduced margins
        layout.setSpacing(2)  # Further reduced spacing
        
        # Output button - centered, no group
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Left stretch
        
        self.output_btn = QPushButton("OFF")
        self.output_btn.setCheckable(True)
        self.output_btn.clicked.connect(self._toggle_output)
        # Width constraints: min=160px, max=free
        self.output_btn.setStyleSheet("""
            QPushButton {
                background-color: #666666;
                color: white;
                font-weight: bold;
                font-size: 12px;
                border: 1px solid #888888;
                border-radius: 4px;
                min-width: 160px;
                min-height: 28px;
            }
            QPushButton:checked {
                background-color: #00aa00;
                border-color: #00cc00;
            }
            QPushButton:hover {
                border-color: #aaaaaa;
            }
        """)
        
        button_layout.addWidget(self.output_btn)
        button_layout.addStretch()  # Right stretch
        
        layout.addLayout(button_layout)
        
        # Setpoint group - compact layout with proper margins
        setpoint_group = QGroupBox("Setpoints")
        setpoint_group.setStyleSheet("QGroupBox { font-size: 10px; }")  # Increased font (+1px)
        setpoint_layout = QFormLayout(setpoint_group)
        setpoint_layout.setContentsMargins(4, 4, 4, 2)  # Reduced top/bottom margins
        setpoint_layout.setVerticalSpacing(2)             # Minimal vertical spacing
        setpoint_layout.setHorizontalSpacing(3)           # Minimal horizontal spacing
        
        # Voltage setpoint - compact
        self.voltage_spin = QDoubleSpinBox()
        self.voltage_spin.setRange(0.0, 64.0)
        self.voltage_spin.setDecimals(3)  # Reduced decimals
        self.voltage_spin.setSingleStep(0.1)
        self.voltage_spin.setValue(0.0)
        self.voltage_spin.setSuffix(" V")
        self.voltage_spin.setMinimumHeight(24)  # Increased height for better usability
        self.voltage_spin.setMaximumHeight(24)
        self.voltage_spin.valueChanged.connect(self._settings_changed)
        
        v_label = QLabel("V:")
        v_label.setStyleSheet("QLabel { font-size: 10px; }")  # Increased font (+1px)
        setpoint_layout.addRow(v_label, self.voltage_spin)
        
        # Current setpoint - compact
        self.current_spin = QDoubleSpinBox()
        self.current_spin.setRange(0.0, 10.0)
        self.current_spin.setDecimals(3)  # Reduced decimals
        self.current_spin.setSingleStep(0.01)
        self.current_spin.setValue(0.0)
        self.current_spin.setSuffix(" A")
        self.current_spin.setMinimumHeight(24)  # Increased height for better usability
        self.current_spin.setMaximumHeight(24)
        self.current_spin.valueChanged.connect(self._settings_changed)
        
        i_label = QLabel("I:")
        i_label.setStyleSheet("QLabel { font-size: 10px; }")  # Increased font (+1px)
        setpoint_layout.addRow(i_label, self.current_spin)
        
        layout.addWidget(setpoint_group)
        
        # Protection group - more compact with proper margins
        protection_group = QGroupBox("Protection")
        protection_group.setStyleSheet("QGroupBox { font-size: 10px; }")  # Increased font (+1px)
        protection_layout = QGridLayout(protection_group)  # Changed to grid for compactness
        protection_layout.setContentsMargins(4, 4, 4, 2)  # Reduced margins
        protection_layout.setHorizontalSpacing(3)  # Minimal horizontal spacing
        protection_layout.setVerticalSpacing(2)    # Minimal vertical spacing
        
        # OVP settings - compact
        self.ovp_enabled_check = QCheckBox("OVP")
        self.ovp_enabled_check.setStyleSheet("QCheckBox { font-size: 9px; }")  # Increased font (+1px)
        self.ovp_enabled_check.stateChanged.connect(self._settings_changed)
        protection_layout.addWidget(self.ovp_enabled_check, 0, 0)
        
        self.ovp_level_spin = QDoubleSpinBox()
        self.ovp_level_spin.setRange(0.0, 66.0)
        self.ovp_level_spin.setDecimals(2)  # Reduced decimals
        self.ovp_level_spin.setSingleStep(0.1)
        self.ovp_level_spin.setValue(6.0)
        self.ovp_level_spin.setSuffix("V")
        self.ovp_level_spin.setMinimumHeight(22)  # Increased height for better usability
        self.ovp_level_spin.setMaximumHeight(22)
        self.ovp_level_spin.valueChanged.connect(self._settings_changed)
        protection_layout.addWidget(self.ovp_level_spin, 0, 1)
        
        # OCP settings - compact
        self.ocp_enabled_check = QCheckBox("OCP")
        self.ocp_enabled_check.setStyleSheet("QCheckBox { font-size: 9px; }")  # Increased font (+1px)
        self.ocp_enabled_check.stateChanged.connect(self._settings_changed)
        protection_layout.addWidget(self.ocp_enabled_check, 1, 0)
        
        self.ocp_level_spin = QDoubleSpinBox()
        self.ocp_level_spin.setRange(0.0, 11.0)
        self.ocp_level_spin.setDecimals(2)  # Reduced decimals
        self.ocp_level_spin.setSingleStep(0.01)
        self.ocp_level_spin.setValue(1.0)
        self.ocp_level_spin.setSuffix("A")
        self.ocp_level_spin.setMinimumHeight(22)  # Increased height for better usability
        self.ocp_level_spin.setMaximumHeight(22)
        self.ocp_level_spin.valueChanged.connect(self._settings_changed)
        protection_layout.addWidget(self.ocp_level_spin, 1, 1)
        
        layout.addWidget(protection_group)
        layout.addStretch()  # Push content to top
    
    def _toggle_output(self):
        """Toggle output state."""
        state = self.output_btn.isChecked()
        self.output_btn.setText("ON" if state else "OFF")  # Shorter text for compact design
        self.output_toggled.emit(self.channel, state)
        self.logger.info(f"Output {'enabled' if state else 'disabled'}")
    
    def _settings_changed(self):
        """Handle settings change."""
        settings = {
            'voltage': self.voltage_spin.value(),
            'current': self.current_spin.value(),
            'ovp_enabled': self.ovp_enabled_check.isChecked(),
            'ovp_level': self.ovp_level_spin.value(),
            'ocp_enabled': self.ocp_enabled_check.isChecked(),
            'ocp_level': self.ocp_level_spin.value()
        }
        
        self.settings_changed.emit(self.channel, settings)
        self.logger.debug(f"Settings changed: {settings}")
    
    
    def update_output_state(self, state: bool):
        """Update output state display."""
        self.output_btn.setChecked(state)
        self.output_btn.setText("Output ON" if state else "Output OFF")


class StatusWidget(QWidget):
    """
    Status monitoring widget for a single channel.
    
    Features:
    - Real-time measurements
    - Protection status
    - Historical statistics
    """
    
    def __init__(self, channel: int):
        super().__init__()
        
        self.channel = channel
        self.measurements_history = []
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup status widget UI."""
        layout = QVBoxLayout(self)
        
        # Current measurements group
        measurements_group = QGroupBox("Current Measurements")
        measurements_layout = QGridLayout(measurements_group)
        
        # Big digit displays
        self.voltage_display = BigDigitDisplay("Voltage", "V", precision=6)
        self.current_display = BigDigitDisplay("Current", "A", precision=6)
        self.power_display = BigDigitDisplay("Power", "W", precision=3)
        
        measurements_layout.addWidget(self.voltage_display, 0, 0)
        measurements_layout.addWidget(self.current_display, 0, 1)
        measurements_layout.addWidget(self.power_display, 0, 2)
        
        layout.addWidget(measurements_group)
        
        # Protection status group
        protection_group = QGroupBox("Protection Status")
        protection_layout = QGridLayout(protection_group)
        
        self.protection_lamps = {
            'ovp': StatusLamp("OVP Status"),
            'ocp': StatusLamp("OCP Status"),
            'output': StatusLamp("Output Enable"),
            'cv_mode': StatusLamp("CV Mode"),
            'cc_mode': StatusLamp("CC Mode")
        }
        
        row = 0
        for lamp in self.protection_lamps.values():
            protection_layout.addWidget(lamp, row, 0)
            row += 1
        
        layout.addWidget(protection_group)
        
        # Statistics group
        stats_group = QGroupBox("Statistics")
        stats_layout = QFormLayout(stats_group)
        
        self.stats_labels = {}
        stats_items = [
            ('min_voltage', 'Min Voltage:'),
            ('max_voltage', 'Max Voltage:'),
            ('avg_voltage', 'Avg Voltage:'),
            ('min_current', 'Min Current:'),
            ('max_current', 'Max Current:'),
            ('avg_current', 'Avg Current:'),
            ('total_energy', 'Total Energy:')
        ]
        
        for key, label in stats_items:
            value_label = QLabel("0.000")
            value_label.setFont(QFont("Courier", 9))
            stats_layout.addRow(label, value_label)
            self.stats_labels[key] = value_label
        
        layout.addWidget(stats_group)
        
        # Add stretch
        layout.addStretch()
    
    def update_measurement(self, measurement: ChannelMeasurement):
        """Update with new measurement."""
        # Update displays
        self.voltage_display.set_value(measurement.voltage)
        self.current_display.set_value(measurement.current)
        self.power_display.set_value(measurement.power)
        
        # Store measurement
        self.measurements_history.append(measurement)
        
        # Keep only recent measurements (last hour at 10Hz = 36000 points)
        if len(self.measurements_history) > 36000:
            self.measurements_history = self.measurements_history[-36000:]
        
        # Update statistics
        self._update_statistics()
    
    def _update_statistics(self):
        """Update statistical displays."""
        if not self.measurements_history:
            return
        
        voltages = [m.voltage for m in self.measurements_history]
        currents = [m.current for m in self.measurements_history]
        powers = [m.power for m in self.measurements_history]
        
        # Calculate statistics
        stats = {
            'min_voltage': min(voltages),
            'max_voltage': max(voltages),
            'avg_voltage': sum(voltages) / len(voltages),
            'min_current': min(currents),
            'max_current': max(currents),
            'avg_current': sum(currents) / len(currents),
        }
        
        # Calculate total energy (approximate)
        if len(self.measurements_history) > 1:
            total_energy = 0.0
            for i in range(1, len(self.measurements_history)):
                dt = (self.measurements_history[i].timestamp - 
                     self.measurements_history[i-1].timestamp)
                energy = self.measurements_history[i].power * dt / 3600  # Wh
                total_energy += energy
            stats['total_energy'] = total_energy
        else:
            stats['total_energy'] = 0.0
        
        # Update labels
        for key, value in stats.items():
            if key in self.stats_labels:
                if 'energy' in key:
                    self.stats_labels[key].setText(f"{value:.3f} Wh")
                else:
                    self.stats_labels[key].setText(f"{value:.6f}")


class TrendWidget(QWidget):
    """
    Trend plotting widget using pyqtgraph.
    
    Features:
    - Real-time plotting
    - Multiple channels
    - Zoom and pan
    - Data export
    """
    
    def __init__(self):
        super().__init__()
        
        self.logger = get_logger('TrendWidget')
        self.plot_data = {1: {'time': [], 'voltage': [], 'current': [], 'power': []},
                         2: {'time': [], 'voltage': [], 'current': [], 'power': []},
                         3: {'time': [], 'voltage': [], 'current': [], 'power': []}}
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup trend plotting UI."""
        layout = QVBoxLayout(self)
        
        if not PYQTGRAPH_AVAILABLE:
            # Fallback to simple text display
            self.info_label = QLabel("PyQtGraph not available. Install with: pip install pyqtgraph")
            self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(self.info_label)
            return
        
        # Create plot widget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('#2b2b2b')
        self.plot_widget.setLabel('left', 'Value')
        self.plot_widget.setLabel('bottom', 'Time', 's')
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        
        # Add legend
        self.plot_widget.addLegend()
        
        # Create plot curves
        self.curves = {}
        colors = ['#ff0000', '#00ff00', '#0000ff']  # Red, Green, Blue
        
        for i, channel in enumerate([1, 2, 3]):
            self.curves[f'ch{channel}_voltage'] = self.plot_widget.plot(
                pen=pg.mkPen(colors[i], width=2), 
                name=f'CH{channel} Voltage'
            )
            self.curves[f'ch{channel}_current'] = self.plot_widget.plot(
                pen=pg.mkPen(colors[i], width=2, style=Qt.PenStyle.DashLine), 
                name=f'CH{channel} Current'
            )
        
        layout.addWidget(self.plot_widget)
        
        # Control panel
        control_panel = QWidget()
        control_layout = QHBoxLayout(control_panel)
        
        # Time span control
        control_layout.addWidget(QLabel("Time span:"))
        self.timespan_combo = QComboBox()
        self.timespan_combo.addItems(["10 sec", "30 sec", "1 min", "5 min", "10 min", "30 min"])
        self.timespan_combo.setCurrentText("30 sec")
        control_layout.addWidget(self.timespan_combo)
        
        # Clear button
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self._clear_data)
        control_layout.addWidget(clear_btn)
        
        # Export button
        export_btn = QPushButton("Export...")
        export_btn.clicked.connect(self._export_data)
        control_layout.addWidget(export_btn)
        
        control_layout.addStretch()
        layout.addWidget(control_panel)
    
    def add_measurement(self, channel: int, measurement: ChannelMeasurement):
        """Add new measurement to trend plot."""
        if not PYQTGRAPH_AVAILABLE:
            return
        
        if channel not in self.plot_data:
            return
        
        # Add data point
        current_time = time.time()
        self.plot_data[channel]['time'].append(current_time)
        self.plot_data[channel]['voltage'].append(measurement.voltage)
        self.plot_data[channel]['current'].append(measurement.current)
        self.plot_data[channel]['power'].append(measurement.power)
        
        # Limit data points based on time span
        timespan_text = self.timespan_combo.currentText()
        if "sec" in timespan_text:
            max_age = int(timespan_text.split()[0])
        elif "min" in timespan_text:
            max_age = int(timespan_text.split()[0]) * 60
        else:
            max_age = 30  # Default 30 seconds
        
        # Remove old data
        cutoff_time = current_time - max_age
        for key in ['time', 'voltage', 'current', 'power']:
            data = self.plot_data[channel][key]
            times = self.plot_data[channel]['time']
            
            # Find cutoff index
            cutoff_index = 0
            for i, t in enumerate(times):
                if t >= cutoff_time:
                    cutoff_index = i
                    break
            
            # Keep recent data
            self.plot_data[channel][key] = data[cutoff_index:]
        
        # Update plot curves
        times = self.plot_data[channel]['time']
        if times:
            # Convert to relative time
            start_time = times[0]
            rel_times = [(t - start_time) for t in times]
            
            self.curves[f'ch{channel}_voltage'].setData(
                rel_times, 
                self.plot_data[channel]['voltage']
            )
            self.curves[f'ch{channel}_current'].setData(
                rel_times, 
                self.plot_data[channel]['current']
            )
    
    def _clear_data(self):
        """Clear all plot data."""
        for channel in [1, 2, 3]:
            for key in ['time', 'voltage', 'current', 'power']:
                self.plot_data[channel][key] = []
        
        # Clear curves
        if PYQTGRAPH_AVAILABLE:
            for curve in self.curves.values():
                curve.setData([], [])
    
    def _export_data(self):
        """Export trend data to CSV."""
        # This would open a file dialog and export data
        # Implementation depends on requirements
        self.logger.info("Export data requested")


class AlarmWidget(QWidget):
    """
    Alarm management widget.
    
    Features:
    - Active alarms list
    - Alarm history
    - Acknowledgment
    - Alarm configuration
    """
    
    def __init__(self):
        super().__init__()
        
        self.active_alarms = []
        self.alarm_history = []
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup alarm widget UI."""
        layout = QVBoxLayout(self)
        
        # Active alarms group
        active_group = QGroupBox("Active Alarms")
        active_layout = QVBoxLayout(active_group)
        
        self.active_list = QListWidget()
        self.active_list.setMaximumHeight(150)
        active_layout.addWidget(self.active_list)
        
        # Alarm buttons
        alarm_btn_layout = QHBoxLayout()
        
        ack_btn = QPushButton("Acknowledge")
        ack_btn.clicked.connect(self._acknowledge_alarm)
        alarm_btn_layout.addWidget(ack_btn)
        
        ack_all_btn = QPushButton("Acknowledge All")
        ack_all_btn.clicked.connect(self._acknowledge_all)
        alarm_btn_layout.addWidget(ack_all_btn)
        
        active_layout.addLayout(alarm_btn_layout)
        layout.addWidget(active_group)
        
        # Alarm history group
        history_group = QGroupBox("Alarm History")
        history_layout = QVBoxLayout(history_group)
        
        self.history_list = QListWidget()
        history_layout.addWidget(self.history_list)
        
        # Clear history button
        clear_history_btn = QPushButton("Clear History")
        clear_history_btn.clicked.connect(self._clear_history)
        history_layout.addWidget(clear_history_btn)
        
        layout.addWidget(history_group)
    
    def add_alarm(self, channel: str, alarm_type: str, message: str = ""):
        """Add new alarm."""
        alarm_text = f"CH{channel}: {alarm_type.upper()}"
        if message:
            alarm_text += f" - {message}"
        
        # Add to active alarms
        if alarm_text not in self.active_alarms:
            self.active_alarms.append(alarm_text)
            self.active_list.addItem(alarm_text)
        
        # Add to history
        timestamp = time.strftime("%H:%M:%S")
        history_text = f"[{timestamp}] {alarm_text}"
        self.alarm_history.append(history_text)
        self.history_list.addItem(history_text)
        
        # Scroll to bottom
        self.history_list.scrollToBottom()
    
    def _acknowledge_alarm(self):
        """Acknowledge selected alarm."""
        current_item = self.active_list.currentItem()
        if current_item:
            alarm_text = current_item.text()
            if alarm_text in self.active_alarms:
                self.active_alarms.remove(alarm_text)
            
            self.active_list.takeItem(self.active_list.row(current_item))
    
    def _acknowledge_all(self):
        """Acknowledge all alarms."""
        self.active_alarms.clear()
        self.active_list.clear()
    
    def _clear_history(self):
        """Clear alarm history."""
        self.alarm_history.clear()
        self.history_list.clear()


# Additional utility functions and classes would continue here...

def create_industrial_button(text: str, color: str = "#4a4a4a") -> QPushButton:
    """Create a standardized industrial-style button."""
    button = QPushButton(text)
    button.setStyleSheet(f"""
        QPushButton {{
            background-color: {color};
            color: white;
            font-weight: bold;
            padding: 8px 16px;
            border: 2px solid #666666;
            border-radius: 4px;
            min-height: 30px;
        }}
        QPushButton:hover {{
            border-color: #888888;
            background-color: {color}dd;
        }}
        QPushButton:pressed {{
            background-color: {color}aa;
        }}
        QPushButton:disabled {{
            background-color: #333333;
            color: #666666;
            border-color: #444444;
        }}
    """)
    return button


class ConnectionDialog(QDialog):
    """
    Connection management dialog.
    
    Standalone dialog for managing instrument connections.
    Replaces the dock-based ConnectionWidget for cleaner UI.
    """
    
    connection_requested = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.logger = get_logger('ConnectionDialog')
        self.available_resources = []
        
        self._setup_ui()
        self._refresh_resources()
    
    def _setup_ui(self):
        """Setup connection dialog UI."""
        self.setWindowTitle("Connection Manager")
        self.setFixedSize(500, 400)
        
        layout = QVBoxLayout(self)
        
        # Header
        header_label = QLabel("DP2031 Instrument Connection")
        header_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setStyleSheet("color: #2196F3; padding: 10px;")
        layout.addWidget(header_label)
        
        # Resource selection group
        resource_group = QGroupBox("Available Resources")
        resource_layout = QVBoxLayout(resource_group)
        
        # Resource list
        resource_info_layout = QHBoxLayout()
        resource_info_layout.addWidget(QLabel("Select instrument resource:"))
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self._refresh_resources)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-weight: bold;
                padding: 5px 10px;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        resource_info_layout.addWidget(refresh_btn)
        resource_layout.addLayout(resource_info_layout)
        
        # Resource combo box
        self.resource_combo = QComboBox()
        self.resource_combo.setEditable(True)
        self.resource_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 2px solid #666666;
                border-radius: 3px;
                background-color: white;
                min-height: 25px;
            }
            QComboBox:focus {
                border-color: #2196F3;
            }
        """)
        resource_layout.addWidget(self.resource_combo)
        
        # Resource examples
        examples_label = QLabel("""
Examples:
• USB: USB0::0x1AB1::0x0E11::DP2D251800XXX::INSTR
• LAN: TCPIP0::192.168.1.120::INSTR  
• RS232: ASRL1::INSTR (COM1)
• GPIB: GPIB0::5::INSTR
        """)
        examples_label.setStyleSheet("color: #666666; font-size: 9pt; padding: 5px;")
        resource_layout.addWidget(examples_label)
        
        layout.addWidget(resource_group)
        
        # Connection parameters group  
        params_group = QGroupBox("Connection Parameters")
        params_layout = QFormLayout(params_group)
        
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(1000, 30000)
        self.timeout_spin.setValue(5000)
        self.timeout_spin.setSuffix(" ms")
        params_layout.addRow("Timeout:", self.timeout_spin)
        
        self.termination_combo = QComboBox()
        self.termination_combo.addItems(["\\n", "\\r\\n", "\\r"])
        params_layout.addRow("Termination:", self.termination_combo)
        
        layout.addWidget(params_group)
        
        # Status display
        self.status_label = QLabel("Ready to connect")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #f0f0f0;
                border: 2px solid #cccccc;
                border-radius: 3px;
                padding: 8px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.status_label)
        
        # Button box
        self.button_box = QDialogButtonBox()
        
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self._connect)
        self.connect_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 8px 20px;
                border: none;
                border-radius: 3px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        
        self.test_btn = QPushButton("Test")
        self.test_btn.clicked.connect(self._test_connection)
        self.test_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                font-weight: bold;
                padding: 8px 20px;
                border: none;
                border-radius: 3px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #666666;
                color: white;
                font-weight: bold;
                padding: 8px 20px;
                border: none;
                border-radius: 3px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)
        
        self.button_box.addButton(self.test_btn, QDialogButtonBox.ButtonRole.ActionRole)
        self.button_box.addButton(self.connect_btn, QDialogButtonBox.ButtonRole.ActionRole)
        self.button_box.addButton(cancel_btn, QDialogButtonBox.ButtonRole.RejectRole)
        
        layout.addWidget(self.button_box)
    
    def _refresh_resources(self):
        """Refresh available VISA resources."""
        self.logger.info("Refreshing VISA resources")
        
        try:
            import pyvisa
            rm = pyvisa.ResourceManager()
            resources = rm.list_resources()
            rm.close()
            
            self.available_resources = list(resources)
            self.resource_combo.clear()
            self.resource_combo.addItems(self.available_resources)
            
            self.status_label.setText(f"Found {len(resources)} resources")
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: #e8f5e8;
                    border: 2px solid #4CAF50;
                    border-radius: 3px;
                    color: #2e7d32;
                    padding: 8px;
                    font-weight: bold;
                }
            """)
            
            self.logger.info(f"Found {len(resources)} VISA resources")
            
        except Exception as e:
            self.logger.error(f"Error refreshing resources: {e}")
            
            self.available_resources = []
            self.resource_combo.clear()
            # Add some common examples for manual entry
            self.resource_combo.addItems([
                "USB0::0x1AB1::0x0E11::DP2D251800XXX::INSTR",
                "TCPIP0::192.168.1.120::INSTR",
                "ASRL1::INSTR"
            ])
            
            self.status_label.setText("VISA backend not available - manual entry only")
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: #fff3e0;
                    border: 2px solid #FF9800;
                    border-radius: 3px;
                    color: #e65100;
                    padding: 8px;
                    font-weight: bold;
                }
            """)
    
    def _test_connection(self):
        """Test connection to selected resource."""
        resource = self.resource_combo.currentText().strip()
        if not resource:
            QMessageBox.warning(self, "Warning", "Please select or enter a resource string")
            return
        
        self.status_label.setText("Testing connection...")
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #e3f2fd;
                border: 2px solid #2196F3;
                border-radius: 3px;
                color: #1565c0;
                padding: 8px;
                font-weight: bold;
            }
        """)
        
        # Disable buttons during test
        self.test_btn.setEnabled(False)
        self.connect_btn.setEnabled(False)
        
        try:
            from ..core.dp2000_scpi import DP2000
            
            dp = DP2000()
            dp.connect(resource, timeout=self.timeout_spin.value())
            
            # Test basic communication
            idn = dp.idn()
            dp.close()
            
            self.status_label.setText(f"Test successful: {idn}")
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: #e8f5e8;
                    border: 2px solid #4CAF50;
                    border-radius: 3px;
                    color: #2e7d32;
                    padding: 8px;
                    font-weight: bold;
                }
            """)
            
            QMessageBox.information(self, "Test Successful", f"Connection test passed!\n\nInstrument ID:\n{idn}")
            
        except Exception as e:
            self.status_label.setText(f"Test failed: {str(e)}")
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: #ffebee;
                    border: 2px solid #f44336;
                    border-radius: 3px;
                    color: #c62828;
                    padding: 8px;
                    font-weight: bold;
                }
            """)
            
            QMessageBox.critical(self, "Test Failed", f"Connection test failed:\n\n{str(e)}")
        
        finally:
            # Re-enable buttons
            self.test_btn.setEnabled(True)
            self.connect_btn.setEnabled(True)
    
    def _connect(self):
        """Connect to selected resource."""
        resource = self.resource_combo.currentText().strip()
        if not resource:
            QMessageBox.warning(self, "Warning", "Please select or enter a resource string")
            return
        
        self.connection_requested.emit(resource)
        self.accept()
    
    def get_selected_resource(self) -> str:
        """Get the currently selected resource."""
        return self.resource_combo.currentText().strip()
