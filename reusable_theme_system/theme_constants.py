"""
Theme Constants - Color Schemes and Sizing Standards
===================================================

Color palettes and sizing constants for professional PyQt6 themes.
"""

# Light Theme Color Scheme
LIGHT_THEME_COLORS = {
    # Main colors
    'background': '#f8f9fa',
    'surface': '#ffffff', 
    'text_primary': '#495057',
    'text_secondary': '#6c757d',
    'text_muted': '#6c757d',
    
    # Interactive colors
    'primary': '#0d6efd',
    'primary_hover': '#0b5ed7', 
    'primary_pressed': '#0a58ca',
    'secondary': '#6c757d',
    'success': '#198754',
    'info': '#0dcaf0',
    'warning': '#ffc107',
    'danger': '#dc3545',
    
    # Borders and separators
    'border': '#dee2e6',
    'border_light': '#e9ecef',
    'border_dark': '#ced4da',
    
    # Interactive states
    'hover_bg': '#e9ecef',
    'active_bg': '#dee2e6',
    'focus_border': '#86b7fe',
    
    # Status colors
    'status_info': '#0d6efd',
    'status_success': '#198754',
    'status_warning': '#fd7e14',
    'status_error': '#dc3545',
    
    # Industrial LCD Display colors
    'lcd_background': '#1a1a1a',      # Dark background
    'lcd_border': '#ffffff',          # White border
    'lcd_digit_color': '#00ff41',     # Bright green digits
    'lcd_label_color': '#e0e0e0',     # Light gray labels
    'lcd_unit_color': '#cccccc'       # Medium gray units
}

# Dark Theme Color Scheme  
DARK_THEME_COLORS = {
    # Main colors
    'background': '#0d1117',
    'surface': '#21262d',
    'text_primary': '#f0f6fc',
    'text_secondary': '#8b949e', 
    'text_muted': '#8b949e',
    
    # Interactive colors
    'primary': '#1f6feb',
    'primary_hover': '#0969da',
    'primary_pressed': '#0550ae',
    'secondary': '#8b949e',
    'success': '#7c3aed',
    'info': '#58a6ff',
    'warning': '#ffa657',
    'danger': '#f85149',
    
    # Borders and separators
    'border': '#21262d',
    'border_light': '#30363d',
    'border_dark': '#161b22',
    
    # Interactive states
    'hover_bg': '#21262d',
    'active_bg': '#30363d', 
    'focus_border': '#58a6ff',
    
    # Status colors
    'status_info': '#58a6ff',
    'status_success': '#7c3aed',
    'status_warning': '#ffa657',
    'status_error': '#f85149',
    
    # Industrial LCD Display colors
    'lcd_background': '#0a0a0a',      # Very dark background
    'lcd_border': '#4a90e2',          # Blue border
    'lcd_digit_color': '#00ccff',     # Cyan digits
    'lcd_label_color': '#ffffff',     # White labels
    'lcd_unit_color': '#cccccc'       # Light gray units
}

# Compact Desktop Sizing for Better Space Utilization
COMMON_SIZES = {
    # Heights - Reduced for more compact interface
    'control_height': '24px',        # Increased back to comfortable size
    'button_height': '20px',         # Reduced from 24px  
    'input_height': '20px',          # Reduced from 24px
    'tab_height': '28px',            # Reduced from 32px
    'toolbar_height': '28px',        # Reduced from 32px
    
    # Widths - Optimized for content
    'min_button_width': '70px',      # Reduced from 80px
    'min_input_width': '100px',      # Reduced from 120px
    'min_label_width': '35px',       # Reduced from 40px
    'preset_label_width': '55px',    # Reduced from 60px
    'status_label_width': '70px',    # Reduced from 80px
    
    # Spacing - Tighter for compact design
    'padding_small': '3px',          # Reduced from 4px
    'padding_medium': '6px',         # Reduced from 8px
    'padding_large': '9px',          # Reduced from 12px
    'margin_small': '2px',           # Same
    'margin_medium': '3px',          # Reduced from 4px
    'margin_large': '6px',           # Reduced from 8px
    
    # Borders - Same for consistency
    'border_radius': '4px',
    'border_radius_large': '6px',
    'border_width': '1px',
    
    # Font sizes - Balanced for readability
    'font_size_small': '11px',       # Increased small font (+1px)
    'font_size_normal': '12px',      # Increased normal font (+1px)  
    'font_size_large': '13px'        # Increased large font (+1px)
}

# SVG Icons (base64 encoded)
SVG_ICONS = {
    'checkmark': 'PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDQuNUw0LjUgOEwxMSAxIiBzdHJva2U9IiNGRkZGRkYiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=',
    'radio_dot': 'PHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgOCA4IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8Y2lyY2xlIGN4PSI0IiBjeT0iNCIgcj0iMyIgZmlsbD0iI0ZGRkZGRiIvPgo8L3N2Zz4K',
    'dropdown_arrow_light': 'PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEyIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDFMNiA2TDExIDEiIHN0cm9rZT0iIzQ5NTA1NyIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+',
    'dropdown_arrow_dark': 'PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEyIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDFMNiA2TDExIDEiIHN0cm9rZT0iI2YwZjZmYyIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+'
}
