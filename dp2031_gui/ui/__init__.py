"""
DP2031 Industrial Power Controller - UI Module

Industrial-grade user interface components for RIGOL DP2000/DP2031 control.

Components:
- MainWindow: Primary application window with dock-based layout
- Industrial Widgets: Specialized controls for industrial applications
- Connection Management: VISA resource discovery and connection
- Channel Control: Per-channel voltage/current/protection settings  
- Status Monitoring: Real-time measurement displays and protection status
- Trend Analysis: Historical data plotting and analysis
- Alarm Management: Alarm handling and notification system

All components follow industrial design principles:
- High contrast for readability
- Clear visual hierarchy
- Robust error handling
- Professional appearance
"""

from .main_window import MainWindow
from .widgets import (
    BigDigitDisplay,
    StatusLamp,
    ConnectionWidget,
    ChannelControlWidget,
    StatusWidget,
    TrendWidget,
    AlarmWidget,
    create_industrial_button
)

__all__ = [
    'MainWindow',
    'BigDigitDisplay',
    'StatusLamp', 
    'ConnectionWidget',
    'ChannelControlWidget',
    'StatusWidget',
    'TrendWidget',
    'AlarmWidget',
    'create_industrial_button'
]

# Version information
__version__ = '1.0.0'
__author__ = 'HUNG - Industrial Automation'
__description__ = 'Industrial Power Controller UI Components'

# UI Configuration constants
UI_CONFIG = {
    'MEASUREMENT_UPDATE_RATE': 10,  # Hz
    'STATUS_UPDATE_RATE': 1,        # Hz
    'TREND_MAX_POINTS': 36000,      # 1 hour at 10Hz
    'ALARM_HISTORY_MAX': 1000,      # Maximum alarm history entries
    'DEFAULT_TIMESPAN': 30,         # Default trend timespan in seconds
    
    # Colors (Industrial theme)
    'COLOR_BACKGROUND': '#2b2b2b',
    'COLOR_WIDGET_BG': '#3c3c3c',
    'COLOR_BORDER': '#666666',
    'COLOR_TEXT': '#ffffff',
    'COLOR_SUCCESS': '#00aa00',
    'COLOR_ERROR': '#cc0000',
    'COLOR_WARNING': '#aa6600',
    'COLOR_INFO': '#0066aa',
    
    # Status lamp colors
    'LAMP_ON': '#00ff00',
    'LAMP_OFF': '#333333',
    'LAMP_ALARM': '#ff0000',
    'LAMP_WARNING': '#ffaa00',
    
    # Display settings
    'FONT_FAMILY': 'Arial',
    'FONT_SIZE_SMALL': 8,
    'FONT_SIZE_NORMAL': 10,
    'FONT_SIZE_LARGE': 12,
    'FONT_SIZE_DISPLAY': 24,
    
    # Widget dimensions
    'BIG_DISPLAY_MIN_WIDTH': 120,
    'BIG_DISPLAY_MIN_HEIGHT': 100,
    'COMPACT_DISPLAY_MIN_WIDTH': 80,
    'COMPACT_DISPLAY_MIN_HEIGHT': 60,
    'STATUS_LAMP_SIZE': 20,
    'BUTTON_MIN_HEIGHT': 30,
    
    # Layout spacing
    'LAYOUT_SPACING': 10,
    'LAYOUT_MARGIN': 5,
    'GROUP_MARGIN': 3
}


def apply_industrial_theme(app):
    """
    Apply industrial theme to entire application.
    
    Args:
        app: QApplication instance
    """
    industrial_stylesheet = """
    /* Main application styling */
    QMainWindow {
        background-color: #2b2b2b;
        color: #ffffff;
    }
    
    /* Dock widgets */
    QDockWidget {
        background-color: #3c3c3c;
        border: 1px solid #666666;
        color: #ffffff;
    }
    
    QDockWidget::title {
        background-color: #4a4a4a;
        padding: 3px;
        border: 1px solid #666666;
    }
    
    /* Group boxes */
    QGroupBox {
        font-weight: bold;
        border: 2px solid #666666;
        border-radius: 3px;
        margin: 3px;
        padding-top: 10px;
        color: #ffffff;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 7px;
        padding: 0 5px 0 5px;
    }
    
    /* Buttons */
    QPushButton {
        background-color: #4a4a4a;
        color: #ffffff;
        font-weight: bold;
        padding: 8px 16px;
        border: 2px solid #666666;
        border-radius: 4px;
        min-height: 30px;
    }
    
    QPushButton:hover {
        border-color: #888888;
        background-color: #5a5a5a;
    }
    
    QPushButton:pressed {
        background-color: #3a3a3a;
    }
    
    QPushButton:disabled {
        background-color: #333333;
        color: #666666;
        border-color: #444444;
    }
    
    /* Input widgets */
    QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
        background-color: #1a1a1a;
        border: 2px solid #666666;
        border-radius: 3px;
        padding: 4px;
        color: #ffffff;
        selection-background-color: #0066aa;
    }
    
    QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
        border-color: #0066aa;
    }
    
    /* Tables and lists */
    QTableWidget, QListWidget {
        background-color: #1a1a1a;
        border: 1px solid #666666;
        color: #ffffff;
        gridline-color: #666666;
    }
    
    QTableWidget::item, QListWidget::item {
        padding: 4px;
        border-bottom: 1px solid #333333;
    }
    
    QTableWidget::item:selected, QListWidget::item:selected {
        background-color: #0066aa;
    }
    
    /* Tab widgets */
    QTabWidget::pane {
        border: 1px solid #666666;
        background-color: #3c3c3c;
    }
    
    QTabBar::tab {
        background-color: #4a4a4a;
        border: 1px solid #666666;
        padding: 5px 10px;
        margin-right: 1px;
        color: #ffffff;
    }
    
    QTabBar::tab:selected {
        background-color: #5a5a5a;
        border-bottom: 2px solid #00aa00;
    }
    
    /* Status bar */
    QStatusBar {
        background-color: #4a4a4a;
        border-top: 1px solid #666666;
        color: #ffffff;
    }
    
    /* Tool bar */
    QToolBar {
        background-color: #4a4a4a;
        border: 1px solid #666666;
        spacing: 3px;
    }
    
    /* Menu bar */
    QMenuBar {
        background-color: #4a4a4a;
        border-bottom: 1px solid #666666;
        color: #ffffff;
    }
    
    QMenuBar::item {
        padding: 4px 8px;
    }
    
    QMenuBar::item:selected {
        background-color: #5a5a5a;
    }
    
    /* Checkboxes */
    QCheckBox {
        color: #ffffff;
        spacing: 5px;
    }
    
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
        border: 2px solid #666666;
        border-radius: 3px;
        background-color: #1a1a1a;
    }
    
    QCheckBox::indicator:checked {
        background-color: #00aa00;
        border-color: #00aa00;
    }
    """
    
    app.setStyleSheet(industrial_stylesheet)


def get_ui_config():
    """
    Get UI configuration dictionary.
    
    Returns:
        dict: UI configuration settings
    """
    return UI_CONFIG.copy()
