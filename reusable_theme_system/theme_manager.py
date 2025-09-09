"""
Theme Manager - Main theming functionality
==========================================

Core theme management for PyQt6 applications with professional styling.
"""

from typing import Dict, List, Optional
from .theme_constants import LIGHT_THEME_COLORS, DARK_THEME_COLORS, COMMON_SIZES, SVG_ICONS
from .industrial_widgets import get_industrial_widget_styles

class ThemeManager:
    """
    Professional theme manager for PyQt6 applications.
    
    Provides consistent theming across all Qt controls with support for
    light and dark themes, interactive states, and professional styling.
    """
    
    def __init__(self):
        self.current_theme = "light"
        self.custom_themes = {}
        
    def add_custom_theme(self, name: str, colors: Dict[str, str]):
        """Add a custom theme color scheme."""
        self.custom_themes[name] = colors
        
    def get_available_themes(self) -> List[str]:
        """Get list of available theme names."""
        base_themes = ["light", "dark"]
        return base_themes + list(self.custom_themes.keys())
        
    def set_theme(self, theme_name: str):
        """Set the current active theme."""
        if theme_name in self.get_available_themes():
            self.current_theme = theme_name
        else:
            raise ValueError(f"Theme '{theme_name}' not found. Available: {self.get_available_themes()}")
            
    def get_theme_colors(self, theme_name: Optional[str] = None) -> Dict[str, str]:
        """Get color scheme for specified theme."""
        if theme_name is None:
            theme_name = self.current_theme
            
        if theme_name == "light":
            return LIGHT_THEME_COLORS
        elif theme_name == "dark":
            return DARK_THEME_COLORS
        elif theme_name in self.custom_themes:
            return self.custom_themes[theme_name]
        else:
            raise ValueError(f"Theme '{theme_name}' not found")

def get_theme_stylesheet(theme_name: str = "light") -> str:
    """
    Get complete CSS stylesheet for specified theme.
    
    Args:
        theme_name: Theme name ("light", "dark", or custom theme)
        
    Returns:
        Complete CSS stylesheet string
    """
    manager = ThemeManager()
    colors = manager.get_theme_colors(theme_name)
    
    if theme_name.lower() == "light":
        return _generate_light_theme_stylesheet(colors)
    elif theme_name.lower() == "dark":
        return _generate_dark_theme_stylesheet(colors)
    else:
        # For custom themes, use light theme structure with custom colors
        return _generate_custom_theme_stylesheet(colors)

def _generate_light_theme_stylesheet(colors: Dict[str, str]) -> str:
    """Generate light theme stylesheet."""
    return f"""
        /* Light Theme - Professional Design */
        QMainWindow {{
            background-color: {colors['background']};
            color: {colors['text_primary']};
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: {COMMON_SIZES['font_size_normal']};
        }}
        
        /* Central Widget and Main Layout */
        QWidget#centralWidget {{
            background-color: {colors['background']};
        }}
        
        /* General Widget Styling */
        QWidget {{
            background-color: {colors['background']};
            color: {colors['text_primary']};
            font-size: {COMMON_SIZES['font_size_normal']};
        }}
        
        /* Buttons */
        QPushButton {{
            background-color: {colors['surface']};
            border: {COMMON_SIZES['border_width']} solid {colors['border']};
            border-radius: {COMMON_SIZES['border_radius']};
            padding: {COMMON_SIZES['padding_medium']} {COMMON_SIZES['padding_large']};
            color: {colors['text_primary']};
            font-weight: 500;
            min-height: {COMMON_SIZES['control_height']};
            font-size: {COMMON_SIZES['font_size_normal']};
            min-width: {COMMON_SIZES['min_button_width']};
        }}
        QPushButton:hover {{
            background-color: {colors['hover_bg']};
            border-color: {colors['border_dark']};
        }}
        QPushButton:pressed {{
            background-color: {colors['active_bg']};
        }}
        
        /* Tab Widget - Compact Design */
        QTabWidget::pane {{
            border: {COMMON_SIZES['border_width']} solid {colors['border']};
            background-color: {colors['background']};  /* Use main background color */
            border-radius: {COMMON_SIZES['border_radius_large']};
            margin-top: 3px;                    /* Reduced from 5px */
        }}
        QTabBar::tab {{
            background-color: {colors['background']};
            border: {COMMON_SIZES['border_width']} solid {colors['border']};
            padding: {COMMON_SIZES['padding_small']} 12px;  /* Reduced horizontal padding */
            margin-right: {COMMON_SIZES['margin_small']};
            border-top-left-radius: {COMMON_SIZES['border_radius']};
            border-top-right-radius: {COMMON_SIZES['border_radius']};
            font-size: {COMMON_SIZES['font_size_normal']};
            min-width: 60px;                    /* Reduced from min_button_width */
            min-height: {COMMON_SIZES['control_height']};
            color: {colors['text_primary']};
        }}
        QTabBar::tab:selected {{
            background-color: {colors['surface']};
            border-bottom-color: {colors['surface']};
            color: {colors['primary']};
            font-weight: 600;
        }}
        QTabBar::tab:hover {{
            background-color: {colors['hover_bg']};
        }}
        
        /* Group Box - Compact Design with Better Layout */
        QGroupBox {{
            font-weight: 600;
            border: 2px solid {colors['border_light']};
            border-radius: {COMMON_SIZES['border_radius_large']};
            margin: 4px 2px;                    /* Better margins for layout */
            padding-top: 12px;                  /* Space for title */
            padding-left: 4px;                  /* Internal padding */
            padding-right: 4px;
            padding-bottom: 4px;
            background-color: {colors['surface']};
            color: {colors['text_primary']};
            font-size: {COMMON_SIZES['font_size_normal']};
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 8px;                          /* Title position */
            padding: 0 4px 0 4px;              /* Title padding */
            background-color: {colors['surface']};
            color: {colors['text_primary']};
            font-weight: 600;
        }}
        
        /* Scroll Area */
        QScrollArea {{
            background-color: {colors['surface']};
            border: {COMMON_SIZES['border_width']} solid {colors['border']};
            border-radius: {COMMON_SIZES['border_radius_large']};
            color: {colors['text_primary']};
        }}
        QScrollArea QWidget {{
            background-color: {colors['surface']};
            color: {colors['text_primary']};
        }}
        QScrollArea QScrollBar:vertical {{
            background-color: {colors['background']};
            border: {COMMON_SIZES['border_width']} solid {colors['border']};
            border-radius: {COMMON_SIZES['border_radius']};
            width: 12px;
        }}
        QScrollArea QScrollBar::handle:vertical {{
            background-color: {colors['text_secondary']};
            border-radius: {COMMON_SIZES['border_radius']};
            min-height: 20px;
        }}
        QScrollArea QScrollBar::handle:vertical:hover {{
            background-color: {colors['text_primary']};
        }}
        
        /* Combo Box */
        QComboBox {{
            background-color: {colors['surface']};
            border: {COMMON_SIZES['border_width']} solid {colors['border_dark']};
            border-radius: 3px;
            padding: {COMMON_SIZES['padding_small']} {COMMON_SIZES['padding_medium']};
            min-width: {COMMON_SIZES['min_input_width']};
            height: {COMMON_SIZES['control_height']};
            font-size: {COMMON_SIZES['font_size_normal']};
            color: {colors['text_primary']};
        }}
        QComboBox:hover {{
            border-color: {colors['focus_border']};
        }}
        QComboBox:focus {{
            border-color: {colors['primary']};
            outline: none;
        }}
        QComboBox::drop-down {{
            border: none;
            width: 20px;
            background-color: {colors['background']};
        }}
        QComboBox::down-arrow {{
            image: url(data:image/svg+xml;base64,{SVG_ICONS['dropdown_arrow_light']});
            width: 12px;
            height: 8px;
        }}
        QComboBox QAbstractItemView {{
            background-color: {colors['surface']};
            color: {colors['text_primary']};
            border: {COMMON_SIZES['border_width']} solid {colors['border']};
            border-radius: {COMMON_SIZES['border_radius']};
            selection-background-color: {colors['primary']};
            selection-color: #ffffff;
            outline: none;
        }}
        
        /* Input Controls */
        QLineEdit, QSpinBox, QDoubleSpinBox {{
            background-color: {colors['surface']};
            border: {COMMON_SIZES['border_width']} solid {colors['border_dark']};
            border-radius: 3px;
            padding: {COMMON_SIZES['padding_small']} {COMMON_SIZES['padding_medium']};
            height: {COMMON_SIZES['control_height']};
            font-size: {COMMON_SIZES['font_size_normal']};
            color: {colors['text_primary']};
            min-width: {COMMON_SIZES['min_input_width']};
        }}
        QLineEdit:hover, QSpinBox:hover, QDoubleSpinBox:hover {{
            border-color: {colors['focus_border']};
        }}
        QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
            border-color: {colors['primary']};
            outline: none;
        }}
        
        /* CheckBox */
        QCheckBox {{
            color: {colors['text_primary']};
            font-size: {COMMON_SIZES['font_size_normal']};
            spacing: 5px;
        }}
        QCheckBox::indicator {{
            width: 16px;
            height: 16px;
            border-radius: 3px;
            border: {COMMON_SIZES['border_width']} solid {colors['border_dark']};
            background-color: {colors['surface']};
        }}
        QCheckBox::indicator:hover {{
            border-color: {colors['focus_border']};
            background-color: {colors['background']};
        }}
        QCheckBox::indicator:checked {{
            background-color: {colors['primary']};
            border-color: {colors['primary']};
            image: url(data:image/svg+xml;base64,{SVG_ICONS['checkmark']});
        }}
        QCheckBox::indicator:checked:hover {{
            background-color: {colors['primary_hover']};
            border-color: {colors['primary_hover']};
        }}
        QCheckBox:disabled {{
            color: {colors['text_secondary']};
        }}
        QCheckBox::indicator:disabled {{
            background-color: {colors['hover_bg']};
            border-color: {colors['border']};
        }}
        
        /* Radio Button */
        QRadioButton {{
            color: {colors['text_primary']};
            font-size: {COMMON_SIZES['font_size_normal']};
            spacing: 5px;
        }}
        QRadioButton::indicator {{
            width: 16px;
            height: 16px;
            border-radius: 8px;
            border: {COMMON_SIZES['border_width']} solid {colors['border_dark']};
            background-color: {colors['surface']};
        }}
        QRadioButton::indicator:hover {{
            border-color: {colors['focus_border']};
            background-color: {colors['background']};
        }}
        QRadioButton::indicator:checked {{
            background-color: {colors['primary']};
            border-color: {colors['primary']};
            image: url(data:image/svg+xml;base64,{SVG_ICONS['radio_dot']});
        }}
        QRadioButton::indicator:checked:hover {{
            background-color: {colors['primary_hover']};
            border-color: {colors['primary_hover']};
        }}
        
        /* Labels */
        QLabel {{
            color: {colors['text_primary']};
            font-size: {COMMON_SIZES['font_size_normal']};
            padding: {COMMON_SIZES['padding_small']};
            min-width: {COMMON_SIZES['min_label_width']};
        }}
        
        QLabel[class="preset-label"] {{
            color: {colors['text_secondary']};
            font-weight: 600;
            margin-right: {COMMON_SIZES['margin_medium']};
            min-width: {COMMON_SIZES['preset_label_width']};
            font-size: {COMMON_SIZES['font_size_normal']};
        }}

        QLabel[class="status-label"] {{
            color: {colors['status_info']};
            font-style: italic;
            padding: {COMMON_SIZES['padding_small']} {COMMON_SIZES['padding_medium']};
            min-width: {COMMON_SIZES['status_label_width']};
            font-size: {COMMON_SIZES['font_size_normal']};
        }}

        QLabel[class="test-label"] {{
            color: {colors['status_success']};
            font-weight: bold;
            padding: {COMMON_SIZES['padding_small']} {COMMON_SIZES['padding_medium']};
            min-width: {COMMON_SIZES['status_label_width']};
            font-size: {COMMON_SIZES['font_size_normal']};
        }}
        
        /* Slider */
        QSlider::groove:horizontal {{
            background-color: {colors['hover_bg']};
            height: 4px;
            border-radius: 2px;
        }}
        QSlider::handle:horizontal {{
            background-color: {colors['primary']};
            width: 16px;
            height: 16px;
            border-radius: 8px;
            margin: -6px 0;
        }}
        QSlider::handle:horizontal:hover {{
            background-color: {colors['primary_hover']};
        }}
        
        /* Status Bar */
        QStatusBar {{
            background-color: {colors['background']};
            border-top: {COMMON_SIZES['border_width']} solid {colors['border']};
            color: {colors['text_secondary']};
            font-size: {COMMON_SIZES['font_size_small']};
        }}
        
        /* ToolBar */
        QToolBar {{
            background-color: {colors['surface']};
            border-bottom: {COMMON_SIZES['border_width']} solid {colors['border']};
            spacing: 3px;
            padding: 5px;
        }}
        
        QAction {{
            color: {colors['text_primary']};
            font-size: {COMMON_SIZES['font_size_normal']};
        }}
        
        QToolBar QToolButton {{
            background-color: transparent;
            color: {colors['text_primary']};
            border: none;
            padding: {COMMON_SIZES['padding_medium']} {COMMON_SIZES['padding_large']};
            border-radius: {COMMON_SIZES['border_radius']};
            margin: {COMMON_SIZES['margin_small']};
            font-size: {COMMON_SIZES['font_size_normal']};
            min-height: {COMMON_SIZES['control_height']};
            min-width: 60px;
        }}
        QToolBar QToolButton:hover {{
            background-color: {colors['hover_bg']};
            color: {colors['primary']};
            border: {COMMON_SIZES['border_width']} solid {colors['border']};
        }}
        QToolBar QToolButton:pressed {{
            background-color: {colors['active_bg']};
            color: {colors['primary_hover']};
            border: {COMMON_SIZES['border_width']} solid {colors['focus_border']};
        }}
        QToolBar QToolButton:checked {{
            background-color: {colors['primary']};
            color: #ffffff;
            border: {COMMON_SIZES['border_width']} solid {colors['primary']};
        }}
        
        /* Menu Bar */
        QMenuBar {{
            background-color: {colors['background']};
            border-bottom: {COMMON_SIZES['border_width']} solid {colors['border']};
            color: {colors['text_primary']};
            font-size: {COMMON_SIZES['font_size_normal']};
        }}
        QMenuBar::item {{
            padding: {COMMON_SIZES['padding_small']} {COMMON_SIZES['padding_medium']};
            border-radius: 3px;
        }}
        QMenuBar::item:selected {{
            background-color: {colors['hover_bg']};
        }}
        
        /* Menu Dropdowns */
        QMenu {{
            background-color: {colors['surface']};
            border: {COMMON_SIZES['border_width']} solid {colors['border_light']};
            border-radius: {COMMON_SIZES['border_radius']};
            padding: {COMMON_SIZES['padding_small']};
            color: {colors['text_primary']};
            font-size: {COMMON_SIZES['font_size_normal']};
        }}
        QMenu::item {{
            padding: {COMMON_SIZES['padding_small']} {COMMON_SIZES['padding_medium']};
            border-radius: 3px;
        }}
        QMenu::item:selected {{
            background-color: {colors['hover_bg']};
            color: {colors['text_primary']};
        }}
        QMenu::separator {{
            height: 1px;
            background: {colors['border_light']};
            margin: {COMMON_SIZES['padding_small']} 0;
        }}
        
        /* Dock Widgets */
        QDockWidget {{
            background-color: {colors['background']};
            color: {colors['text_primary']};
            border: {COMMON_SIZES['border_width']} solid {colors['border_light']};
            titlebar-close-icon: none;
            titlebar-normal-icon: none;
        }}
        QDockWidget::title {{
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 {colors['surface']}, stop: 1 {colors['background']});
            border-bottom: {COMMON_SIZES['border_width']} solid {colors['border_light']};
            padding: {COMMON_SIZES['padding_small']} {COMMON_SIZES['padding_medium']};
            color: {colors['text_primary']};
            font-weight: bold;
            font-size: {COMMON_SIZES['font_size_normal']};
        }}
        QDockWidget::close-button, QDockWidget::float-button {{
            background: {colors['surface']};
            border: 1px solid {colors['border_light']};
            border-radius: 3px;
            width: 14px;
            height: 14px;
        }}
        QDockWidget::close-button:hover, QDockWidget::float-button:hover {{
            background: {colors['danger']};
            border-color: {colors['danger']};
        }}
        
        {get_industrial_widget_styles(colors, COMMON_SIZES)}
    """

def _generate_dark_theme_stylesheet(colors: Dict[str, str]) -> str:
    """Generate dark theme stylesheet."""
    return f"""
        /* Dark Theme - Professional Design */
        QMainWindow {{
            background-color: {colors['background']};
            color: {colors['text_primary']};
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: {COMMON_SIZES['font_size_normal']};
        }}
        
        /* Central Widget and Main Layout */
        QWidget#centralWidget {{
            background-color: {colors['background']};
        }}
        
        /* General Widget Styling */
        QWidget {{
            background-color: {colors['background']};
            color: {colors['text_primary']};
            font-size: {COMMON_SIZES['font_size_normal']};
        }}
        
        /* Buttons */
        QPushButton {{
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 {colors['surface']}, stop: 1 {colors['border_dark']});
            border: {COMMON_SIZES['border_width']} solid {colors['border_light']};
            border-radius: {COMMON_SIZES['border_radius']};
            padding: {COMMON_SIZES['padding_medium']} {COMMON_SIZES['padding_large']};
            color: {colors['text_primary']};
            font-weight: 500;
            min-height: {COMMON_SIZES['control_height']};
            font-size: {COMMON_SIZES['font_size_normal']};
            min-width: {COMMON_SIZES['min_button_width']};
        }}
        QPushButton:hover {{
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 {colors['border_light']}, stop: 1 {colors['surface']});
            border-color: {colors['info']};
            color: {colors['info']};
        }}
        QPushButton:pressed {{
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 {colors['border_dark']}, stop: 1 {colors['background']});
            border-color: {colors['primary']};
        }}
        
        /* Tab Widget - Compact Design */
        QTabWidget::pane {{
            border: {COMMON_SIZES['border_width']} solid {colors['surface']};
            background-color: {colors['background']};
            border-radius: {COMMON_SIZES['border_radius_large']};
            margin-top: 3px;                    /* Reduced from 5px */
        }}
        QTabBar::tab {{
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 {colors['surface']}, stop: 1 {colors['border_dark']});
            border: {COMMON_SIZES['border_width']} solid {colors['border_light']};
            padding: {COMMON_SIZES['padding_small']} 12px;  /* Reduced horizontal padding */
            margin-right: {COMMON_SIZES['margin_small']};
            border-top-left-radius: {COMMON_SIZES['border_radius']};
            border-top-right-radius: {COMMON_SIZES['border_radius']};
            font-size: {COMMON_SIZES['font_size_normal']};
            min-width: 60px;                    /* Reduced from min_button_width */
            min-height: {COMMON_SIZES['control_height']};
            color: {colors['text_secondary']};
        }}
        QTabBar::tab:selected {{
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 {colors['primary']}, stop: 1 {colors['primary_hover']});
            border-bottom-color: {colors['background']};
            color: #ffffff;
            font-weight: 600;
        }}
        QTabBar::tab:hover {{
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 {colors['border_light']}, stop: 1 {colors['surface']});
            color: {colors['info']};
            border-color: {colors['info']};
        }}
        
        /* Group Box - Compact Design with Better Layout */
        QGroupBox {{
            font-weight: 600;
            border: 2px solid {colors['surface']};
            border-radius: {COMMON_SIZES['border_radius_large']};
            margin: 4px 2px;                    /* Better margins for layout */
            padding-top: 12px;                  /* Space for title */
            padding-left: 4px;                  /* Internal padding */
            padding-right: 4px;
            padding-bottom: 4px;
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 {colors['border_dark']}, stop: 1 {colors['background']});
            color: {colors['text_primary']};
            font-size: {COMMON_SIZES['font_size_normal']};
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 8px;                          /* Title position */
            padding: 0 4px 0 4px;              /* Title padding */
            background-color: {colors['surface']};
            color: {colors['warning']};
            font-weight: 600;
        }}
        
        /* Scroll Area */
        QScrollArea {{
            background-color: {colors['background']};
            border: {COMMON_SIZES['border_width']} solid {colors['surface']};
            border-radius: {COMMON_SIZES['border_radius_large']};
            color: {colors['text_primary']};
        }}
        QScrollArea QWidget {{
            background-color: {colors['background']};
            color: {colors['text_primary']};
        }}
        QScrollArea QScrollBar:vertical {{
            background-color: {colors['surface']};
            border: {COMMON_SIZES['border_width']} solid {colors['border_light']};
            border-radius: {COMMON_SIZES['border_radius']};
            width: 12px;
        }}
        QScrollArea QScrollBar::handle:vertical {{
            background-color: {colors['text_secondary']};
            border-radius: {COMMON_SIZES['border_radius']};
            min-height: 20px;
        }}
        QScrollArea QScrollBar::handle:vertical:hover {{
            background-color: {colors['text_primary']};
        }}
        
        /* Combo Box */
        QComboBox {{
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 {colors['surface']}, stop: 1 {colors['border_dark']});
            border: {COMMON_SIZES['border_width']} solid {colors['border_light']};
            border-radius: 3px;
            padding: {COMMON_SIZES['padding_small']} {COMMON_SIZES['padding_medium']};
            min-width: {COMMON_SIZES['min_input_width']};
            height: {COMMON_SIZES['control_height']};
            font-size: {COMMON_SIZES['font_size_normal']};
            color: {colors['text_primary']};
        }}
        QComboBox:hover {{
            border-color: {colors['info']};
            color: {colors['info']};
        }}
        QComboBox:focus {{
            border-color: {colors['primary']};
            outline: none;
        }}
        QComboBox::drop-down {{
            border: none;
            width: 20px;
            background-color: {colors['surface']};
        }}
        QComboBox::down-arrow {{
            image: url(data:image/svg+xml;base64,{SVG_ICONS['dropdown_arrow_dark']});
            width: 12px;
            height: 8px;
        }}
        QComboBox QAbstractItemView {{
            background-color: {colors['surface']};
            color: {colors['text_primary']};
            border: {COMMON_SIZES['border_width']} solid {colors['border_light']};
            border-radius: {COMMON_SIZES['border_radius']};
            selection-background-color: {colors['primary']};
            selection-color: #ffffff;
            outline: none;
        }}
        
        /* Input Controls */
        QLineEdit, QSpinBox, QDoubleSpinBox {{
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 {colors['surface']}, stop: 1 {colors['border_dark']});
            border: {COMMON_SIZES['border_width']} solid {colors['border_light']};
            border-radius: 3px;
            padding: {COMMON_SIZES['padding_small']} {COMMON_SIZES['padding_medium']};
            height: {COMMON_SIZES['control_height']};
            font-size: {COMMON_SIZES['font_size_normal']};
            color: {colors['text_primary']};
            min-width: {COMMON_SIZES['min_input_width']};
        }}
        QLineEdit:hover, QSpinBox:hover, QDoubleSpinBox:hover {{
            border-color: {colors['info']};
        }}
        QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
            border-color: {colors['primary']};
            outline: none;
        }}
        
        /* CheckBox */
        QCheckBox {{
            color: {colors['text_primary']};
            font-size: {COMMON_SIZES['font_size_normal']};
            spacing: 5px;
        }}
        QCheckBox::indicator {{
            width: 16px;
            height: 16px;
            border-radius: 3px;
            border: {COMMON_SIZES['border_width']} solid {colors['border_light']};
            background-color: {colors['surface']};
        }}
        QCheckBox::indicator:hover {{
            border-color: {colors['info']};
            background-color: {colors['border_dark']};
        }}
        QCheckBox::indicator:checked {{
            background-color: {colors['primary']};
            border-color: {colors['primary']};
            image: url(data:image/svg+xml;base64,{SVG_ICONS['checkmark']});
        }}
        QCheckBox::indicator:checked:hover {{
            background-color: {colors['primary_hover']};
            border-color: {colors['primary_hover']};
        }}
        QCheckBox:disabled {{
            color: {colors['text_secondary']};
        }}
        QCheckBox::indicator:disabled {{
            background-color: {colors['border_dark']};
            border-color: {colors['surface']};
        }}
        
        /* Radio Button */
        QRadioButton {{
            color: {colors['text_primary']};
            font-size: {COMMON_SIZES['font_size_normal']};
            spacing: 5px;
        }}
        QRadioButton::indicator {{
            width: 16px;
            height: 16px;
            border-radius: 8px;
            border: {COMMON_SIZES['border_width']} solid {colors['border_light']};
            background-color: {colors['surface']};
        }}
        QRadioButton::indicator:hover {{
            border-color: {colors['info']};
            background-color: {colors['border_dark']};
        }}
        QRadioButton::indicator:checked {{
            background-color: {colors['primary']};
            border-color: {colors['primary']};
            image: url(data:image/svg+xml;base64,{SVG_ICONS['radio_dot']});
        }}
        QRadioButton::indicator:checked:hover {{
            background-color: {colors['primary_hover']};
            border-color: {colors['primary_hover']};
        }}
        
        /* Labels */
        QLabel {{
            color: {colors['text_primary']};
            font-size: {COMMON_SIZES['font_size_normal']};
            padding: {COMMON_SIZES['padding_small']};
            min-width: {COMMON_SIZES['min_label_width']};
        }}
        
        QLabel[class="preset-label"] {{
            color: {colors['text_secondary']};
            font-weight: 600;
            margin-right: {COMMON_SIZES['margin_medium']};
            min-width: {COMMON_SIZES['preset_label_width']};
            font-size: {COMMON_SIZES['font_size_normal']};
        }}

        QLabel[class="status-label"] {{
            color: {colors['status_info']};
            font-style: italic;
            padding: {COMMON_SIZES['padding_small']} {COMMON_SIZES['padding_medium']};
            min-width: {COMMON_SIZES['status_label_width']};
            font-size: {COMMON_SIZES['font_size_normal']};
        }}

        QLabel[class="test-label"] {{
            color: {colors['status_success']};
            font-weight: bold;
            padding: {COMMON_SIZES['padding_small']} {COMMON_SIZES['padding_medium']};
            min-width: {COMMON_SIZES['status_label_width']};
            font-size: {COMMON_SIZES['font_size_normal']};
        }}
        
        /* Slider */
        QSlider::groove:horizontal {{
            background-color: {colors['surface']};
            height: 4px;
            border-radius: 2px;
        }}
        QSlider::handle:horizontal {{
            background-color: {colors['info']};
            width: 16px;
            height: 16px;
            border-radius: 8px;
            margin: -6px 0;
        }}
        QSlider::handle:horizontal:hover {{
            background-color: {colors['primary']};
        }}
        
        /* Status Bar */
        QStatusBar {{
            background-color: {colors['background']};
            border-top: {COMMON_SIZES['border_width']} solid {colors['surface']};
            color: {colors['text_secondary']};
            font-size: {COMMON_SIZES['font_size_small']};
        }}
        
        /* ToolBar */
        QToolBar {{
            background-color: {colors['border_dark']};
            border-bottom: {COMMON_SIZES['border_width']} solid {colors['surface']};
            spacing: 3px;
            padding: 5px;
        }}
        
        QAction {{
            color: {colors['text_primary']};
            font-size: {COMMON_SIZES['font_size_normal']};
        }}
        
        QToolBar QToolButton {{
            background-color: transparent;
            color: {colors['text_primary']};
            border: none;
            padding: {COMMON_SIZES['padding_medium']} {COMMON_SIZES['padding_large']};
            border-radius: {COMMON_SIZES['border_radius']};
            margin: {COMMON_SIZES['margin_small']};
            font-size: {COMMON_SIZES['font_size_normal']};
            min-height: {COMMON_SIZES['control_height']};
            min-width: 60px;
        }}
        QToolBar QToolButton:hover {{
            background-color: {colors['surface']};
            color: {colors['info']};
            border: {COMMON_SIZES['border_width']} solid {colors['border_light']};
        }}
        QToolBar QToolButton:pressed {{
            background-color: {colors['border_light']};
            color: {colors['primary']};
            border: {COMMON_SIZES['border_width']} solid {colors['info']};
        }}
        QToolBar QToolButton:checked {{
            background-color: {colors['primary']};
            color: #ffffff;
            border: {COMMON_SIZES['border_width']} solid {colors['primary']};
        }}
        
        /* Menu Bar */
        QMenuBar {{
            background-color: {colors['background']};
            border-bottom: {COMMON_SIZES['border_width']} solid {colors['surface']};
            color: {colors['text_primary']};
            font-size: {COMMON_SIZES['font_size_normal']};
        }}
        QMenuBar::item {{
            padding: {COMMON_SIZES['padding_small']} {COMMON_SIZES['padding_medium']};
            border-radius: 3px;
        }}
        QMenuBar::item:selected {{
            background-color: {colors['surface']};
        }}
        
        /* Menu Dropdowns */
        QMenu {{
            background-color: {colors['surface']};
            border: {COMMON_SIZES['border_width']} solid {colors['border_light']};
            border-radius: {COMMON_SIZES['border_radius']};
            padding: {COMMON_SIZES['padding_small']};
            color: {colors['text_primary']};
            font-size: {COMMON_SIZES['font_size_normal']};
        }}
        QMenu::item {{
            padding: {COMMON_SIZES['padding_small']} {COMMON_SIZES['padding_medium']};
            border-radius: 3px;
        }}
        QMenu::item:selected {{
            background-color: {colors['border_light']};
            color: {colors['text_primary']};
        }}
        QMenu::separator {{
            height: 1px;
            background: {colors['border_light']};
            margin: {COMMON_SIZES['padding_small']} 0;
        }}
        
        /* Dock Widgets */
        QDockWidget {{
            background-color: {colors['background']};
            color: {colors['text_primary']};
            border: {COMMON_SIZES['border_width']} solid {colors['border_light']};
            titlebar-close-icon: none;
            titlebar-normal-icon: none;
        }}
        QDockWidget::title {{
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 {colors['surface']}, stop: 1 {colors['background']});
            border-bottom: {COMMON_SIZES['border_width']} solid {colors['border_light']};
            padding: {COMMON_SIZES['padding_small']} {COMMON_SIZES['padding_medium']};
            color: {colors['text_primary']};
            font-weight: bold;
            font-size: {COMMON_SIZES['font_size_normal']};
        }}
        QDockWidget::close-button, QDockWidget::float-button {{
            background: {colors['surface']};
            border: 1px solid {colors['border_light']};
            border-radius: 3px;
            width: 14px;
            height: 14px;
        }}
        QDockWidget::close-button:hover, QDockWidget::float-button:hover {{
            background: {colors['danger']};
            border-color: {colors['danger']};
        }}
        
        {get_industrial_widget_styles(colors, COMMON_SIZES)}
    """

def _generate_custom_theme_stylesheet(colors: Dict[str, str]) -> str:
    """Generate custom theme stylesheet using light theme structure."""
    # For custom themes, use the light theme structure with custom colors
    return _generate_light_theme_stylesheet(colors)

def apply_theme_to_application(app, theme_name: str = "light"):
    """
    Apply theme to QApplication instance.
    
    Args:
        app: QApplication instance
        theme_name: Theme name to apply
    """
    stylesheet = get_theme_stylesheet(theme_name)
    app.setStyleSheet(stylesheet)

def get_available_themes() -> List[str]:
    """Get list of available theme names."""
    return ["light", "dark"]
