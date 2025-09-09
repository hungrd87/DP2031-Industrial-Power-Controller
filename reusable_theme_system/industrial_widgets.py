"""
Industrial Widget Styles for DP2031 Theme System
==============================================

Additional styles for industrial display widgets used in the DP2031 application.
"""

def get_industrial_widget_styles(colors, sizes):
    """Get industrial widget specific styling."""
    return f"""
        /* Industrial Value Display */
        QLabel#industrial-value {{
            background-color: {colors['surface']};
            border: 2px solid {colors['border']};
            border-radius: {sizes['border_radius']};
            padding: {sizes['padding_medium']};
            color: {colors['primary']};
            font-family: 'Courier New', monospace;
            font-weight: bold;
        }}
        
        /* Industrial Status Lamps */
        QLabel#industrial-lamp-on {{
            background-color: {colors['success']};
            border: 2px solid {colors['border']};
            border-radius: 50%;
            min-width: 16px;
            max-width: 16px;
            min-height: 16px;
            max-height: 16px;
        }}
        
        QLabel#industrial-lamp-off {{
            background-color: {colors['hover_bg']};
            border: 2px solid {colors['border']};
            border-radius: 50%;
            min-width: 16px;
            max-width: 16px;
            min-height: 16px;
            max-height: 16px;
        }}
        
        /* Industrial Connection Buttons */
        QPushButton#connect-button {{
            background-color: {colors['success']};
            color: white;
            border: 2px solid {colors['success']};
            font-weight: bold;
        }}
        
        QPushButton#connect-button:hover {{
            background-color: {colors['success']};
            border-color: {colors['success']};
        }}
        
        QPushButton#disconnect-button {{
            background-color: {colors['danger']};
            color: white;
            border: 2px solid {colors['danger']};
            font-weight: bold;
        }}
        
        QPushButton#disconnect-button:hover {{
            background-color: {colors['danger']};
            border-color: {colors['danger']};
        }}
        
        /* Industrial Output Button */
        QPushButton#output-button-on {{
            background-color: {colors['success']};
            color: white;
            border: 2px solid {colors['success']};
            font-weight: bold;
        }}
        
        QPushButton#output-button-off {{
            background-color: {colors['hover_bg']};
            color: {colors['text_primary']};
            border: 2px solid {colors['border']};
            font-weight: bold;
        }}
        
        /* Channel Headers */
        QLabel#channel-header {{
            background-color: {colors['primary']};
            color: white;
            padding: {sizes['padding_medium']};
            font-weight: bold;
            border-radius: {sizes['border_radius']};
        }}
        
        /* Emergency Stop in Toolbar */
        QToolBar QToolButton[text="EMERGENCY STOP"] {{
            color: #dc3545;
            font-weight: bold;
            font-size: 12px;
            padding: 8px 12px;
            background-color: transparent;
            border: 2px solid transparent;
        }}
        
        QToolBar QToolButton[text="EMERGENCY STOP"]:hover {{
            background-color: #dc35451a;
            border: 2px solid #dc3545;
            border-radius: 4px;
        }}
        
        QToolBar QToolButton[text="EMERGENCY STOP"]:pressed {{
            background-color: #dc354533;
            border: 2px solid #dc3545;
        }}
    """
