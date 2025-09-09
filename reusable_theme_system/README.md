# RTB2000 Professional Theme System - Usage Guide

## 📋 Overview

This is a complete, reusable PyQt6 theme system extracted from the RTB2000 project. It provides professional light and dark themes with consistent styling across all Qt controls.

## 🎨 Features

- **Professional Design**: Desktop-standard sizing and modern appearance
- **Complete Coverage**: All Qt controls styled consistently
- **Interactive States**: Proper hover/pressed/checked feedback
- **SVG Icons**: High-quality modern icons for checkboxes and radio buttons
- **Easy Integration**: Simple API for any PyQt6 project
- **Customizable**: Add your own color schemes

## 🚀 Quick Start

### 1. Basic Usage

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from reusable_theme_system import get_theme_stylesheet

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Themed App")
        
        # Apply theme
        stylesheet = get_theme_stylesheet("light")  # or "dark"
        self.setStyleSheet(stylesheet)
        
        # Your UI code here
        button = QPushButton("Themed Button")
        self.setCentralWidget(button)

app = QApplication(sys.argv)
window = MyApp()
window.show()
app.exec()
```

### 2. Runtime Theme Switching

```python
from reusable_theme_system import get_theme_stylesheet

class ThemedApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_theme = "light"
        self.setup_ui()
        
    def switch_theme(self):
        # Toggle between light and dark
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        stylesheet = get_theme_stylesheet(self.current_theme)
        self.setStyleSheet(stylesheet)
```

### 3. Using Label Classes

```python
# Create labels with special styling
normal_label = QLabel("Normal text")

preset_label = QLabel("Setting:")
preset_label.setProperty("class", "preset-label")  # Muted color

status_label = QLabel("Status: Connected")
status_label.setProperty("class", "status-label")  # Blue color

result_label = QLabel("Test: PASSED")
result_label.setProperty("class", "test-label")  # Green/Purple color
```

## 📁 Installation

### Method 1: Copy Directory
1. Copy the `reusable_theme_system` directory to your project
2. Import and use as shown in examples

### Method 2: Add to Python Path
```python
import sys
sys.path.append('path/to/reusable_theme_system')
from reusable_theme_system import get_theme_stylesheet
```

### Method 3: Package Installation
```bash
# If you want to create a pip package (advanced)
cd reusable_theme_system
python setup.py install
```

## 🛠️ API Reference

### Core Functions

#### `get_theme_stylesheet(theme_name: str) -> str`
Returns complete CSS stylesheet for the specified theme.

**Parameters:**
- `theme_name`: "light", "dark", or custom theme name

**Returns:**
- CSS stylesheet string

#### `apply_theme_to_application(app, theme_name: str)`
Apply theme directly to QApplication instance.

**Parameters:**
- `app`: QApplication instance
- `theme_name`: Theme name to apply

#### `get_available_themes() -> List[str]`
Get list of available theme names.

**Returns:**
- List of theme names

### Theme Manager Class

#### `ThemeManager()`
Advanced theme management with custom theme support.

```python
from reusable_theme_system import ThemeManager

manager = ThemeManager()

# Add custom theme
custom_colors = {
    'background': '#f0f0f0',
    'text_primary': '#333333',
    # ... more colors
}
manager.add_custom_theme('my_theme', custom_colors)

# Use custom theme
stylesheet = manager.get_theme_stylesheet('my_theme')
```

## 🎨 Color Schemes

### Light Theme
- **Background**: `#f8f9fa` (Light gray)
- **Surface**: `#ffffff` (White)
- **Text Primary**: `#495057` (Dark gray)
- **Primary**: `#0d6efd` (Blue)
- **Success**: `#198754` (Green)

### Dark Theme
- **Background**: `#0d1117` (Dark)
- **Surface**: `#21262d` (Dark gray)
- **Text Primary**: `#f0f6fc` (Light)
- **Primary**: `#1f6feb` (Blue)
- **Success**: `#7c3aed` (Purple)

## 📏 Sizing Standards

- **Control Height**: 24px (desktop standard)
- **Button Min Width**: 80px
- **Input Min Width**: 120px
- **Font Size**: 11px (normal)
- **Border Radius**: 4px
- **Padding**: 4px-12px

## 🧩 Supported Controls

### Input Controls
- `QPushButton` - Professional styling with hover effects
- `QLineEdit` - Consistent height and focus states
- `QSpinBox`, `QDoubleSpinBox` - Themed spin buttons
- `QComboBox` - Custom dropdown arrows and item styling
- `QSlider` - Modern handle design

### Selection Controls
- `QCheckBox` - SVG checkmarks with proper states
- `QRadioButton` - SVG radio dots with hover effects
- Both support disabled states

### Layout Controls
- `QTabWidget` - Professional tab styling
- `QGroupBox` - Themed borders and titles
- `QScrollArea` - Themed background and scroll bars
- `QToolBar` - Professional action button styling

### Text Controls
- `QLabel` - Multiple classes (normal, preset, status, test)
- Proper text colors for all themes

## 💡 Best Practices

### 1. Use Fusion Style
```python
app = QApplication(sys.argv)
app.setStyle('Fusion')  # Recommended for best results
```

### 2. Apply Theme Early
Apply theme before showing windows for best visual consistency.

### 3. Label Classes
Use semantic label classes for consistent styling:
```python
# Good
label.setProperty("class", "status-label")

# Avoid manual styling
label.setStyleSheet("color: blue;")  # Don't do this
```

### 4. Theme Switching
For smooth theme transitions, apply to the main window:
```python
main_window.setStyleSheet(get_theme_stylesheet(theme_name))
```

## 🔧 Customization

### Custom Colors
```python
from reusable_theme_system import ThemeManager, LIGHT_THEME_COLORS

# Create custom theme based on light theme
custom_colors = LIGHT_THEME_COLORS.copy()
custom_colors['primary'] = '#ff6b35'  # Orange primary
custom_colors['success'] = '#28a745'  # Custom green

manager = ThemeManager()
manager.add_custom_theme('orange', custom_colors)
```

### Custom Sizing
Modify `COMMON_SIZES` in `theme_constants.py` for different sizing standards.

## 🧪 Testing

Run the example application:
```bash
cd reusable_theme_system
python example_usage.py
```

This demonstrates all features and serves as a comprehensive test.

## 📝 Requirements

- Python 3.7+
- PyQt6
- No additional dependencies

## 🤝 Contributing

This theme system was extracted from the RTB2000 project. Feel free to:
- Report issues
- Suggest improvements
- Add new themes
- Extend control support

## 📄 License

MIT License - Free to use in any project.

## 🎯 Examples

See `example_usage.py` for a complete demonstration application showing all features.

---

**Happy Theming!** 🎨✨
