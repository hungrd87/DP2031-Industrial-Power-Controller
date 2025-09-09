"""
Main window for DP2031 Industrial Power Controller.

Simplified industrial-style interface with:
- Central control dashboard
- Channel control panel (docked)
- Status monitoring (floating, hidden by default)
- Alarm management (floating, hidden by default)  
- Connection via Tools menu dialog

Features clean, focused design with essential controls prominently displayed.
"""

import sys
import time
from typing import Dict, List, Optional
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QDockWidget, QTabWidget, QSplitter, QStatusBar, QMenuBar,
    QMenu, QToolBar, QLabel, QPushButton, QGroupBox, QFrame,
    QApplication, QMessageBox, QDialog, QTextEdit, QProgressBar,
    QSizePolicy
)
from PyQt6.QtCore import (
    Qt, QTimer, QThread, pyqtSignal, QSettings, QSize, QPoint
)
from PyQt6.QtGui import QAction, QIcon, QFont, QPixmap, QPalette, QColor, QActionGroup

from ..core.dp2000_scpi import DP2000
from ..core.model import ChannelMeasurement, ProtectionSettings, PowerSupplyModel
from ..core.logging_cfg import get_logger
from .widgets import (
    ChannelControlWidget, StatusWidget, AlarmWidget, 
    BigDigitDisplay, StatusLamp, ConnectionDialog
)

# Import reusable theme system
try:
    # Try direct import first
    from reusable_theme_system.theme_manager import ThemeManager, get_theme_stylesheet
except ImportError:
    # Fallback to path modification
    import sys
    import os
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    sys.path.insert(0, os.path.join(project_root, 'reusable_theme_system'))
    from theme_manager import ThemeManager, get_theme_stylesheet


class MainWindow(QMainWindow):
    """
    Main application window with industrial dock-based layout.
    
    Provides comprehensive control interface for DP2000/DP2031 power supplies
    with real-time monitoring, trending, and alarm management.
    """
    
    # Signals
    connection_status_changed = pyqtSignal(bool)
    measurement_updated = pyqtSignal(int, ChannelMeasurement)
    alarm_triggered = pyqtSignal(str, str)  # channel, alarm_type
    shutdown_requested = pyqtSignal()  # Signal for application shutdown
    
    def __init__(self):
        """Initialize main window with industrial layout."""
        super().__init__()
        
        self.logger = get_logger('MainWindow')
        self.logger.info("Initializing DP2031 Main Window")
        
        # Core components
        self.dp2000: Optional[DP2000] = None
        self.power_supply_model = PowerSupplyModel()
        self.settings = QSettings('RIGOL', 'DP2031_Controller')
        self.last_resource = None  # Store last connected resource
        
        # Theme manager
        self.theme_manager = ThemeManager()
        
        # UI components
        self.dock_widgets: Dict[str, QDockWidget] = {}
        self.channel_widgets: Dict[int, ChannelControlWidget] = {}
        self.status_widgets: Dict[int, StatusWidget] = {}
        
        # Timers
        self.measurement_timer = QTimer()
        self.status_timer = QTimer()
        
        # Initialize UI
        self._setup_ui()
        self._setup_docks()
        self._setup_menu_bar()
        self._setup_tool_bar()
        self._setup_status_bar()
        self._setup_timers()
        self._load_settings()
        
        # Connect signals
        self.connection_status_changed.connect(self._update_connect_action)
        
        # Load and apply theme
        self._load_theme()
        
        # Industrial styling is now handled by the theme manager
        
        self.logger.info("Main window initialization completed")
    
    def _setup_ui(self):
        """Setup main window properties and central widget."""
        self.setWindowTitle("DP2031 Industrial Power Controller")
        self.setMinimumSize(800, 450)  # Further reduced minimum height to 450px
        self.resize(1000, 500)  # Reduced default height to 500px

        # Set window icon (if available)
        try:
            self.setWindowIcon(QIcon("resources/dp2031_icon.png"))
        except:
            pass
        
        # Central widget with main layout
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")  # Set object name for theme styling
        self.setCentralWidget(central_widget)
        
        # Main horizontal layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Left side: Channel control tabs (fixed position)
        self._create_channel_control_tabs(main_layout)
        
        # Right side: Dashboard panels in TabWidget
        dashboard_widget = QWidget()
        dashboard_widget.setObjectName("dashboardWidget")  # Set object name for theme styling
        dashboard_layout = QVBoxLayout(dashboard_widget)
        dashboard_layout.setSpacing(5)
        dashboard_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create TabWidget for dashboard panels
        dashboard_tabs = QTabWidget()
        dashboard_tabs.setObjectName("dashboardTabs")
        
        # Quick status tab (moved to first position)
        status_widget = QWidget()
        self._create_quick_status_panel_content(status_widget)
        dashboard_tabs.addTab(status_widget, "Channel Status")
        
        # System overview tab (moved to second position)
        overview_widget = QWidget()
        self._create_overview_panel_content(overview_widget)
        dashboard_tabs.addTab(overview_widget, "System Overview")
        
        dashboard_layout.addWidget(dashboard_tabs)
        
        main_layout.addWidget(dashboard_widget, 2)  # Give dashboard more space
    
    def _create_channel_control_tabs(self, parent_layout: QHBoxLayout):
        """Create channel control tabs with fixed position and compact size."""
        # Create tab widget for channels
        self.channel_tabs = QTabWidget()
        self.channel_tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.channel_tabs.setMinimumWidth(300)  # Reduced from 400
        # self.channel_tabs.setMaximumWidth(380)  # Reduced from 500
        
        # Apply compact styling for industrial look
        # TabWidget styling is now handled by the theme manager
        
        # Create channel control widgets
        for channel in [1, 2, 3]:
            channel_widget = ChannelControlWidget(channel)
            channel_widget.settings_changed.connect(self._handle_channel_settings_changed)
            channel_widget.output_toggled.connect(self._handle_output_toggle)
            
            self.channel_widgets[channel] = channel_widget
            self.channel_tabs.addTab(channel_widget, f"Channel {channel}")
        
        # Add to layout
        parent_layout.addWidget(self.channel_tabs, 1)  # Give tabs less space than dashboard
    
    def _create_overview_panel_content(self, parent_widget: QWidget):
        """Create system overview panel content for tab."""
        layout = QVBoxLayout(parent_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        # Remove GroupBox wrapper, just add content directly
        overview_layout = QGridLayout()
        
        # System identification
        self.system_id_label = QLabel("Disconnected")
        self.system_id_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.system_id_label.setStyleSheet("color: #cc0000; padding: 5px;")
        overview_layout.addWidget(QLabel("Instrument:"), 0, 0)
        overview_layout.addWidget(self.system_id_label, 0, 1, 1, 2)
        
        # Connection status lamp
        self.connection_lamp = StatusLamp("Connection")
        self.connection_lamp.set_state(False)
        overview_layout.addWidget(self.connection_lamp, 0, 3)
        
        # Total power display
        self.total_power_display = BigDigitDisplay("Total Power", "W", precision=2)
        overview_layout.addWidget(self.total_power_display, 1, 0, 2, 2)
        
        # System status indicators
        status_frame = QFrame()
        status_layout = QVBoxLayout(status_frame)
        
        self.system_status_lamps = {
            'output_enabled': StatusLamp("Output Enable"),
            'protection_ok': StatusLamp("Protection OK"),
            'communication_ok': StatusLamp("Communication"),
            'measurement_ok': StatusLamp("Measurements")
        }
        
        for lamp in self.system_status_lamps.values():
            status_layout.addWidget(lamp)
        
        overview_layout.addWidget(status_frame, 1, 2, 2, 2)
        
        # Add overview layout to main layout
        layout.addLayout(overview_layout)
        layout.addStretch()  # Push content to top
    
    def _create_quick_status_panel_content(self, parent_widget: QWidget):
        """Create quick status panel content for tab."""
        layout = QVBoxLayout(parent_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        # Remove GroupBox wrapper, just add content directly
        quick_status_layout = QHBoxLayout()
        
        # Create mini status widgets for each channel
        self.quick_status_widgets = {}
        for channel in [1, 2, 3]:
            channel_frame = QFrame()
            channel_frame.setFrameStyle(QFrame.Shape.Box)
            channel_layout = QVBoxLayout(channel_frame)
            
            # Channel label
            channel_label = QLabel(f"CH{channel}")
            channel_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            channel_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            channel_layout.addWidget(channel_label)
            
            # Mini displays
            voltage_display = BigDigitDisplay("V", "", precision=3, compact=True)
            current_display = BigDigitDisplay("A", "", precision=3, compact=True)
            power_display = BigDigitDisplay("W", "", precision=2, compact=True)
            
            channel_layout.addWidget(voltage_display)
            channel_layout.addWidget(current_display)
            channel_layout.addWidget(power_display)
            
            # Output status lamp
            output_lamp = StatusLamp("Output")
            channel_layout.addWidget(output_lamp)
            
            self.quick_status_widgets[channel] = {
                'voltage': voltage_display,
                'current': current_display,
                'power': power_display,
                'output': output_lamp
            }
            
            quick_status_layout.addWidget(channel_frame)
        
        # Add quick status layout to main layout
        layout.addLayout(quick_status_layout)
        layout.addStretch()  # Push content to top
    
    def _setup_docks(self):
        """Setup dock widgets for different functional areas."""
        self.logger.info("Setting up dock widgets")
        
        # Only create floating docks now (channels are in main layout)
        
        # Status monitoring dock (right side, floating)
        self._create_status_dock()
        
        # Alarm management dock (right side, floating)
        self._create_alarm_dock()
        
        # Configure floating docks
        self._configure_floating_docks()
    def _create_status_dock(self):
        """Create status monitoring dock (floating, hidden by default)."""
        status_dock = QDockWidget("Status Monitoring", self)
        status_dock.setObjectName("StatusDock")
        status_dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QDockWidget.DockWidgetFeature.DockWidgetFloatable |
            QDockWidget.DockWidgetFeature.DockWidgetClosable
        )
        
        # Create main container widget
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Create tab widget for status pages
        status_tabs = QTabWidget()
        
        # Channel status tabs
        for channel in [1, 2, 3]:
            status_widget = StatusWidget(channel)
            self.status_widgets[channel] = status_widget
            status_tabs.addTab(status_widget, f"CH{channel} Status")
        
        # System status tab
        system_status_widget = self._create_system_status_widget()
        status_tabs.addTab(system_status_widget, "System Status")
        
        # Add TabWidget to main layout
        main_layout.addWidget(status_tabs)
        
        # Monitoring Control Buttons (at bottom of dock)
        control_group = QGroupBox("Monitoring Control")
        control_layout = QHBoxLayout(control_group)
        
        self.start_monitoring_btn = QPushButton("Start Monitoring")
        self.start_monitoring_btn.clicked.connect(self._start_monitoring)
        self.start_monitoring_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: 2px solid #28a745;
                padding: 8px 16px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:disabled {
                background-color: #6c757d;
                border-color: #6c757d;
            }
        """)
        
        self.stop_monitoring_btn = QPushButton("Stop Monitoring")
        self.stop_monitoring_btn.clicked.connect(self._stop_monitoring)
        self.stop_monitoring_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: 2px solid #dc3545;
                padding: 8px 16px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:disabled {
                background-color: #6c757d;
                border-color: #6c757d;
            }
        """)
        
        control_layout.addWidget(self.start_monitoring_btn)
        control_layout.addWidget(self.stop_monitoring_btn)
        
        # Add control group to main layout
        main_layout.addWidget(control_group)
        
        # Set the main widget as dock content
        status_dock.setWidget(main_widget)
        
        # Make it floating and hidden by default
        status_dock.setFloating(True)
        status_dock.hide()
        status_dock.resize(400, 350)  # Slightly taller for the buttons
        
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, status_dock)
        self.dock_widgets['status'] = status_dock
    
    def _create_alarm_dock(self):
        """Create alarm management dock (floating, hidden by default)."""
        alarm_dock = QDockWidget("Alarm Management", self)
        alarm_dock.setObjectName("AlarmDock")
        alarm_dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QDockWidget.DockWidgetFeature.DockWidgetFloatable |
            QDockWidget.DockWidgetFeature.DockWidgetClosable
        )
        
        self.alarm_widget = AlarmWidget()
        alarm_dock.setWidget(self.alarm_widget)
        
        # Make it floating and hidden by default
        alarm_dock.setFloating(True)
        alarm_dock.hide()
        alarm_dock.resize(350, 250)
        
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, alarm_dock)
        self.dock_widgets['alarms'] = alarm_dock
    
    def _configure_floating_docks(self):
        """Configure floating docks positioning."""
        # Position floating docks nicely
        main_geometry = self.geometry()
        
        if 'status' in self.dock_widgets:
            status_dock = self.dock_widgets['status']
            status_dock.move(main_geometry.x() + main_geometry.width() - 420, main_geometry.y() + 100)
        
        if 'alarms' in self.dock_widgets:
            alarm_dock = self.dock_widgets['alarms']
            alarm_dock.move(main_geometry.x() + main_geometry.width() - 370, main_geometry.y() + 420)
    
    def _create_system_status_widget(self):
        """Create system-wide status monitoring widget."""
        system_widget = QWidget()
        layout = QVBoxLayout(system_widget)
        
        # Communication statistics
        comm_group = QGroupBox("Communication Statistics")
        comm_layout = QGridLayout(comm_group)
        
        self.comm_stats_labels = {}
        stats_items = [
            ('commands_sent', 'Commands Sent:'),
            ('responses_received', 'Responses Received:'),
            ('errors', 'Errors:'),
            ('reconnections', 'Reconnections:'),
            ('connection_time', 'Connected Time:')
        ]
        
        for i, (key, label) in enumerate(stats_items):
            comm_layout.addWidget(QLabel(label), i, 0)
            value_label = QLabel("0")
            value_label.setFont(QFont("Courier", 10))
            comm_layout.addWidget(value_label, i, 1)
            self.comm_stats_labels[key] = value_label
        
        layout.addWidget(comm_group)
        
        # System health indicators
        health_group = QGroupBox("System Health")
        health_layout = QVBoxLayout(health_group)
        
        self.health_progress = QProgressBar()
        self.health_progress.setRange(0, 100)
        self.health_progress.setValue(100)
        health_layout.addWidget(QLabel("Overall Health:"))
        health_layout.addWidget(self.health_progress)
        
        layout.addWidget(health_group)
        
        return system_widget
    
    def _setup_menu_bar(self):
        """Setup application menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        # Export actions
        export_config_action = QAction("Export &Configuration...", self)
        export_config_action.triggered.connect(self._export_configuration)
        file_menu.addAction(export_config_action)
        
        import_config_action = QAction("&Import Configuration...", self)
        import_config_action.triggered.connect(self._import_configuration)
        file_menu.addAction(import_config_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        # Theme selection
        theme_menu = view_menu.addMenu("&Theme")
        
        # Theme action group for mutual exclusivity
        theme_group = QActionGroup(self)
        
        # Dark theme action
        dark_action = QAction("&Dark Theme", self)
        dark_action.setCheckable(True)
        dark_action.setChecked(self.theme_manager.current_theme == "dark")
        dark_action.triggered.connect(lambda: self._set_theme("dark"))
        theme_group.addAction(dark_action)
        theme_menu.addAction(dark_action)
        
        # Light theme action
        light_action = QAction("&Light Theme", self)
        light_action.setCheckable(True)
        light_action.setChecked(self.theme_manager.current_theme == "light")
        light_action.triggered.connect(lambda: self._set_theme("light"))
        theme_group.addAction(light_action)
        theme_menu.addAction(light_action)
        
        view_menu.addSeparator()
        
        # Toolbar visibility
        toolbar_action = QAction("&Toolbar", self)
        toolbar_action.setCheckable(True)
        toolbar_action.setChecked(True)  # Toolbar should be visible by default
        toolbar_action.triggered.connect(self._toggle_toolbar)
        view_menu.addAction(toolbar_action)
        
        # Dock visibility actions (only for remaining docks)
        for name, dock in self.dock_widgets.items():
            if name in ['status', 'alarms']:  # Only floating docks
                action = dock.toggleViewAction()
                view_menu.addAction(action)
        
        view_menu.addSeparator()
        
        # Layout actions
        reset_layout_action = QAction("&Reset Layout", self)
        reset_layout_action.triggered.connect(self._reset_layout)
        view_menu.addAction(reset_layout_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("&Tools")
        
        # Connection action (NEW)
        connection_action = QAction("&Connection...", self)
        connection_action.setShortcut("Ctrl+O")
        connection_action.triggered.connect(self._show_connection_dialog)
        tools_menu.addAction(connection_action)
        
        tools_menu.addSeparator()
        
        device_info_action = QAction("Device &Information...", self)
        device_info_action.triggered.connect(self._show_device_info)
        tools_menu.addAction(device_info_action)
        
        calibration_action = QAction("&Calibration...", self)
        calibration_action.triggered.connect(self._show_calibration_dialog)
        tools_menu.addAction(calibration_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About...", self)
        about_action.triggered.connect(self._show_about_dialog)
        help_menu.addAction(about_action)
    
    def _setup_tool_bar(self):
        """Setup application toolbar."""
        toolbar = self.addToolBar("Main")
        toolbar.setObjectName("MainToolBar")
        toolbar.setMovable(False)
        toolbar.setVisible(True)  # Ensure toolbar is always visible
        
        # Connect/Disconnect action (checkable)
        self.connect_action = QAction("Connect", self)
        self.connect_action.setToolTip("Connect to power supply")
        self.connect_action.setCheckable(True)
        self.connect_action.triggered.connect(self._toggle_connection)
        toolbar.addAction(self.connect_action)
        
        toolbar.addSeparator()
        
        # Add spacer to push EMERGENCY STOP to the right
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        toolbar.addWidget(spacer)
        
        # Emergency stop with bold red text styling (right side)
        self.emergency_stop_action = QAction("EMERGENCY STOP", self)
        self.emergency_stop_action.setToolTip("Emergency stop - disable all outputs")
        self.emergency_stop_action.triggered.connect(self._emergency_stop)
        toolbar.addAction(self.emergency_stop_action)
        
        # Force toolbar visibility after settings restore
        toolbar = self.findChild(QToolBar, "MainToolBar")
        if toolbar:
            toolbar.setVisible(True)
    
    def _setup_status_bar(self):
        """Setup application status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Connection status
        self.connection_status_label = QLabel("Disconnected")
        self.status_bar.addWidget(self.connection_status_label)
        
        # Measurement rate
        self.measurement_rate_label = QLabel("Rate: 0 Hz")
        self.status_bar.addPermanentWidget(self.measurement_rate_label)
        
        # Time display
        self.time_label = QLabel()
        self.status_bar.addPermanentWidget(self.time_label)
        
        # Update time every second
        time_timer = QTimer()
        time_timer.timeout.connect(self._update_time_display)
        time_timer.start(1000)
    
    def _setup_timers(self):
        """Setup measurement and status update timers."""
        # Measurement timer - 10 Hz default
        self.measurement_timer.timeout.connect(self._update_measurements)
        
        # Status timer - 1 Hz
        self.status_timer.timeout.connect(self._update_status)
        self.status_timer.start(1000)
    
    def _load_settings(self):
        """Load application settings."""
        self.logger.info("Loading application settings")
        
        # Window geometry
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        
        # Window state (dock positions)
        state = self.settings.value("windowState")
        if state:
            self.restoreState(state)
            
        # Ensure toolbar is always visible after state restore
        toolbar = self.findChild(QToolBar, "MainToolBar")
        if toolbar:
            toolbar.setVisible(True)
        
        # Measurement rate
        rate = self.settings.value("measurement_rate", 10, type=int)
        if rate > 0:
            self.measurement_timer.setInterval(1000 // rate)
        
        # Last resource
        self.last_resource = self.settings.value("last_resource", None, type=str)
    
    def _save_settings(self):
        """Save application settings."""
        self.logger.info("Saving application settings")
        
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        
        # Calculate measurement rate from timer interval
        if self.measurement_timer.interval() > 0:
            rate = 1000 // self.measurement_timer.interval()
            self.settings.setValue("measurement_rate", rate)
        
        # Save last resource
        if self.last_resource:
            self.settings.setValue("last_resource", self.last_resource)
    
    # Event handlers
    def _handle_connection_request(self, resource_name: str):
        """Handle instrument connection request."""
        self.logger.info(f"Connection requested: {resource_name}")
        
        try:
            # Create DP2000 instance if needed
            if self.dp2000 is None:
                self.dp2000 = DP2000()
            
            # Attempt connection
            success = self.dp2000.connect(resource_name)
            
            if success:
                # Save the successful resource
                self.last_resource = resource_name
                
                # Update UI
                idn = self.dp2000.get_identification()
                self.system_id_label.setText(f"{idn['model']} - {idn['serial_number']}")
                self.system_id_label.setStyleSheet("color: #00aa00; padding: 5px;")
                
                self.connection_lamp.set_state(True)
                self.connection_status_label.setText(f"Connected: {resource_name}")
                
                # Update power supply model
                self.power_supply_model.model = idn['model']
                self.power_supply_model.serial_number = idn['serial_number']
                self.power_supply_model.firmware_version = idn['firmware_version']
                
                # Start monitoring
                self._start_monitoring()
                
                # Update Connect action state
                self.connect_action.setChecked(True)
                self.connect_action.setText("Disconnect")
                self.connect_action.setToolTip("Disconnect from power supply")
                
                self.connection_status_changed.emit(True)
                self.logger.info("Connection established successfully")
                
            else:
                self._handle_connection_failure("Failed to connect to instrument")
                
        except Exception as e:
            self._handle_connection_failure(f"Connection error: {str(e)}")
    
    def _handle_disconnection_request(self):
        """Handle instrument disconnection request."""
        self.logger.info("Disconnection requested")
        
        try:
            # Stop monitoring
            self._stop_monitoring()
            
            # Disconnect instrument
            if self.dp2000:
                self.dp2000.disconnect()
            
            # Update UI
            self.system_id_label.setText("Disconnected")
            self.system_id_label.setStyleSheet("color: #cc0000; padding: 5px;")
            
            self.connection_lamp.set_state(False)
            self.connection_status_label.setText("Disconnected")
            
            # Reset status lamps
            for lamp in self.system_status_lamps.values():
                lamp.set_state(False)
            
            self.connection_status_changed.emit(False)
            self.logger.info("Disconnection completed")
            
        except Exception as e:
            self.logger.error(f"Disconnection error: {e}")
    
    def _handle_connection_failure(self, message: str):
        """Handle connection failure."""
        self.logger.error(f"Connection failed: {message}")
        
        # Update Connect action state
        self.connect_action.setChecked(False)
        
        # Update UI
        self.system_id_label.setText("Connection Failed")
        self.system_id_label.setStyleSheet("color: #cc0000; padding: 5px;")
        
        self.connection_lamp.set_state(False)
        self.connection_status_label.setText("Connection Failed")
        
        # Show error message
        QMessageBox.critical(self, "Connection Error", message)
    
    def _handle_channel_settings_changed(self, channel: int, settings: dict):
        """Handle channel settings change."""
        self.logger.info(f"Channel {channel} settings changed: {settings}")
        
        if not self.dp2000 or not self.dp2000.is_connected:
            return
        
        try:
            # Apply voltage and current settings
            if 'voltage' in settings:
                self.dp2000.set_voltage(channel, settings['voltage'])
            
            if 'current' in settings:
                self.dp2000.set_current(channel, settings['current'])
            
            # Apply protection settings
            if 'ovp_enabled' in settings and 'ovp_level' in settings:
                self.dp2000.set_ovp_state(channel, settings['ovp_enabled'])
                if settings['ovp_enabled']:
                    self.dp2000.set_ovp_level(channel, settings['ovp_level'])
            
            if 'ocp_enabled' in settings and 'ocp_level' in settings:
                self.dp2000.set_ocp_state(channel, settings['ocp_enabled'])
                if settings['ocp_enabled']:
                    self.dp2000.set_ocp_level(channel, settings['ocp_level'])
            
        except Exception as e:
            self.logger.error(f"Failed to apply channel {channel} settings: {e}")
            QMessageBox.warning(self, "Settings Error", f"Failed to apply settings: {str(e)}")
    
    def _handle_output_toggle(self, channel: int, state: bool):
        """Handle output toggle request."""
        self.logger.info(f"Channel {channel} output {'enabled' if state else 'disabled'}")
        
        if not self.dp2000 or not self.dp2000.is_connected:
            return
        
        try:
            self.dp2000.set_output_state(channel, state)
            
            # Update quick status
            if channel in self.quick_status_widgets:
                self.quick_status_widgets[channel]['output'].set_state(state)
            
        except Exception as e:
            self.logger.error(f"Failed to set channel {channel} output: {e}")
            QMessageBox.warning(self, "Output Error", f"Failed to set output: {str(e)}")
    
    def _start_monitoring(self):
        """Start measurement and status monitoring."""
        if self.dp2000 and self.dp2000.is_connected:
            self.measurement_timer.start()
            self.logger.info("Monitoring started")
    
    def _stop_monitoring(self):
        """Stop measurement and status monitoring."""
        self.measurement_timer.stop()
        self.logger.info("Monitoring stopped")
    
    def _start_monitoring(self):
        """Start measurement and status monitoring."""
        if self.dp2000 and self.dp2000.is_connected:
            self.measurement_timer.start()
            self.logger.info("Monitoring started")
    
    def _stop_monitoring(self):
        """Stop measurement and status monitoring."""
        self.measurement_timer.stop()
        self.logger.info("Monitoring stopped")
    
    def _update_measurements(self):
        """Update measurements from all channels."""
        if not self.dp2000 or not self.dp2000.is_connected:
            return
        
        try:
            total_power = 0.0
            
            for channel in [1, 2, 3]:
                # Get measurement
                measurement = self.dp2000.measure_all(channel)
                
                # Update model
                self.power_supply_model.update_channel_measurement(channel, measurement)
                
                # Update quick status displays
                if channel in self.quick_status_widgets:
                    widgets = self.quick_status_widgets[channel]
                    widgets['voltage'].set_value(measurement.voltage)
                    widgets['current'].set_value(measurement.current)
                    widgets['power'].set_value(measurement.power)
                
                # Emit signal
                self.measurement_updated.emit(channel, measurement)
                
                total_power += measurement.power
            
            # Update total power display
            self.total_power_display.set_value(total_power)
            
            # Update measurement rate display
            rate = 1000 // self.measurement_timer.interval() if self.measurement_timer.interval() > 0 else 0
            self.measurement_rate_label.setText(f"Rate: {rate} Hz")
            
        except Exception as e:
            self.logger.error(f"Measurement update error: {e}")
    
    def _update_status(self):
        """Update status information."""
        if not self.dp2000 or not self.dp2000.is_connected:
            return
        
        try:
            # Update communication statistics
            if hasattr(self.dp2000, 'visa_session'):
                stats = self.dp2000.visa_session.get_statistics()
                
                for key, label in self.comm_stats_labels.items():
                    if key in stats:
                        if key == 'connection_time':
                            # Format time nicely
                            seconds = int(stats[key])
                            hours = seconds // 3600
                            minutes = (seconds % 3600) // 60
                            secs = seconds % 60
                            label.setText(f"{hours:02d}:{minutes:02d}:{secs:02d}")
                        else:
                            label.setText(str(stats[key]))
            
            # Update system status lamps
            self.system_status_lamps['communication_ok'].set_state(True)
            self.system_status_lamps['measurement_ok'].set_state(True)
            
            # Check output states
            output_enabled = False
            protection_ok = True
            
            for channel in [1, 2, 3]:
                if self.dp2000.get_output_state(channel):
                    output_enabled = True
                
                if self.dp2000.check_protection_status(channel):
                    protection_ok = False
                    self.alarm_triggered.emit(str(channel), "protection")
            
            self.system_status_lamps['output_enabled'].set_state(output_enabled)
            self.system_status_lamps['protection_ok'].set_state(protection_ok)
            
        except Exception as e:
            self.logger.error(f"Status update error: {e}")
            self.system_status_lamps['communication_ok'].set_state(False)
    
    def _update_time_display(self):
        """Update time display in status bar."""
        current_time = time.strftime("%H:%M:%S")
        self.time_label.setText(current_time)
    
    def _disconnect_device(self):
        """Disconnect from device and update UI state."""
        try:
            if self.dp2000 and hasattr(self.dp2000, 'disconnect'):
                self.dp2000.disconnect()
                self.logger.info("Disconnected from device")
            
            # Update Connect action state
            self.connect_action.setChecked(False)
            self.connect_action.setText("Connect")
            self.connect_action.setToolTip("Connect to power supply")
            
            # Update status
            self.status_bar.showMessage("Disconnected")
            
        except Exception as e:
            self.logger.error(f"Error during disconnect: {e}")
            QMessageBox.critical(self, "Disconnect Error", f"Error disconnecting: {e}")
    
    def _emergency_stop(self):
        """Emergency stop - disable all outputs immediately."""
        self.logger.warning("EMERGENCY STOP activated")
        
        if not self.dp2000 or not self.dp2000.is_connected:
            return
        
        try:
            # Disable all outputs
            for channel in [1, 2, 3]:
                self.dp2000.set_output_state(channel, False)
            
            # Show confirmation
            QMessageBox.warning(
                self, 
                "Emergency Stop", 
                "All outputs have been disabled!"
            )
            
            self.logger.info("Emergency stop completed")
            
        except Exception as e:
            self.logger.error(f"Emergency stop error: {e}")
            QMessageBox.critical(
                self,
                "Emergency Stop Error",
                f"Failed to disable outputs: {str(e)}"
            )
    
    # Dialog methods
    def _toggle_connection(self):
        """Toggle connection state - Connect/Disconnect."""
        if self.connect_action.isChecked():
            # User clicked to connect
            if self.last_resource:
                # Try to connect with last resource directly
                self.logger.info(f"Attempting to connect to last resource: {self.last_resource}")
                self._handle_connection_request(self.last_resource)
            else:
                # No last resource - show connection dialog
                self.logger.info("No last resource found - showing connection dialog")
                self._show_connection_dialog()
        else:
            # User clicked to disconnect
            self._disconnect_device()
    
    def _show_connection_dialog(self):
        """Show connection dialog."""
        dialog = ConnectionDialog(self)
        dialog.connection_requested.connect(self._handle_connection_request)
        
        result = dialog.exec()
        if result != QDialog.DialogCode.Accepted:
            # Dialog was cancelled - uncheck Connect action
            self.connect_action.setChecked(False)
    
    def _export_configuration(self):
        """Export current configuration to file."""
        self.logger.info("Configuration export requested")
        QMessageBox.information(self, "Export Configuration", "Configuration export feature coming soon!")
    
    def _import_configuration(self):
        """Import configuration from file."""
        self.logger.info("Configuration import requested")
        QMessageBox.information(self, "Import Configuration", "Configuration import feature coming soon!")
    
    def _toggle_toolbar(self, visible: bool):
        """Toggle toolbar visibility"""
        toolbar = self.findChild(QToolBar, "MainToolBar")
        if toolbar:
            toolbar.setVisible(visible)
    
    def _update_connect_action(self, connected: bool):
        """Update connect action text and behavior based on connection status"""
        if connected:
            self.connect_action.setText("Disconnect")
            self.connect_action.setToolTip("Disconnect from power supply")
            self.connect_action.triggered.disconnect()
            self.connect_action.triggered.connect(self._handle_disconnection_request)
        else:
            self.connect_action.setText("Connect")
            self.connect_action.setToolTip("Connect to power supply")
            self.connect_action.triggered.disconnect()
            self.connect_action.triggered.connect(self._show_connection_dialog)
    
    def _reset_layout(self):
        """Reset dock widget layout to default."""
        self.logger.info("Layout reset requested")
        # This would restore default dock positions
        QMessageBox.information(self, "Reset Layout", "Layout reset feature coming soon!")
    
    def _show_calibration_dialog(self):
        """Show calibration dialog."""
        self.logger.info("Calibration dialog requested")
        QMessageBox.information(self, "Calibration", "Calibration feature coming soon!")
    
    def _show_device_info(self):
        """Show device information dialog."""
        if not self.dp2000 or not self.dp2000.is_connected:
            QMessageBox.information(self, "Device Information", "No device connected.")
            return
        
        try:
            idn = self.dp2000.get_identification()
            
            info_text = f"""
            Device Information:
            
            Manufacturer: {idn['manufacturer']}
            Model: {idn['model']}
            Serial Number: {idn['serial_number']}
            Firmware Version: {idn['firmware_version']}
            
            Communication Statistics:
            """
            
            if hasattr(self.dp2000, 'visa_session'):
                stats = self.dp2000.visa_session.get_statistics()
                for key, value in stats.items():
                    info_text += f"\n{key.replace('_', ' ').title()}: {value}"
            
            dialog = QDialog(self)
            dialog.setWindowTitle("Device Information")
            dialog.setModal(True)
            dialog.resize(400, 300)
            
            layout = QVBoxLayout(dialog)
            text_edit = QTextEdit()
            text_edit.setPlainText(info_text)
            text_edit.setReadOnly(True)
            layout.addWidget(text_edit)
            
            button = QPushButton("Close")
            button.clicked.connect(dialog.accept)
            layout.addWidget(button)
            
            dialog.exec()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to get device information: {str(e)}")
    
    def _show_about_dialog(self):
        """Show about dialog."""
        about_text = """
        DP2031 Industrial Power Controller
        Version 1.0.0
        
        Professional control software for RIGOL DP2000/DP2031 power supplies.
        
        Features:
        • Real-time monitoring and control
        • Industrial-grade interface
        • Comprehensive protection management
        • Data logging and trending
        • Alarm management
        
        Built with PyQt6 and PyVISA
        """
        
        QMessageBox.about(self, "About DP2031 Controller", about_text)
    
    def _set_theme(self, theme_name: str):
        """Set application theme using reusable theme system."""
        try:
            # Set theme in manager
            self.theme_manager.set_theme(theme_name)
            
            # Apply stylesheet
            app = QApplication.instance()
            if app:
                stylesheet = get_theme_stylesheet(theme_name)
                app.setStyleSheet(stylesheet)
            
            self.logger.info(f"Theme changed to: {theme_name}")
            
            # Save theme preference
            settings = QSettings()
            settings.setValue("theme", theme_name)
            
        except Exception as e:
            self.logger.error(f"Failed to set theme {theme_name}: {e}")
            QMessageBox.warning(self, "Theme Error", f"Failed to apply {theme_name} theme: {e}")
    
    def _load_theme(self):
        """Load theme from settings using reusable theme system."""
        try:
            settings = QSettings()
            saved_theme = settings.value("theme", "dark")  # Default to dark
            
            # Set theme in manager
            self.theme_manager.set_theme(saved_theme)
            
            # Apply stylesheet  
            app = QApplication.instance()
            if app:
                stylesheet = get_theme_stylesheet(saved_theme)
                app.setStyleSheet(stylesheet)
                
            self.logger.info(f"Loaded theme: {saved_theme}")
        except Exception as e:
            self.logger.warning(f"Failed to load theme, using default: {e}")
            # Fallback to dark theme
            self.theme_manager.set_theme("dark")
            app = QApplication.instance()
            if app:
                stylesheet = get_theme_stylesheet("dark")
                app.setStyleSheet(stylesheet)
    
    # Additional methods would continue here...
    
    def closeEvent(self, event):
        """Handle application close event."""
        self.logger.info("Application closing")
        
        # Emit shutdown signal
        self.shutdown_requested.emit()
        
        # Save settings
        self._save_settings()
        
        # Stop monitoring
        self._stop_monitoring()
        
        # Disconnect instrument
        if self.dp2000:
            self.dp2000.disconnect()
        
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("DP2031 Industrial Power Controller")
    app.setApplicationVersion("1.0.0")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
