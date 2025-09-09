"""
Example: Using RTB2000 Reusable Theme System
============================================

Demonstrates how to integrate the professional theme system 
into any PyQt6 application.
"""

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QWidget, QPushButton, QLabel, QCheckBox, QRadioButton,
                             QComboBox, QLineEdit, QSpinBox, QGroupBox, QTabWidget,
                             QScrollArea, QSlider, QToolBar)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

# Import the reusable theme system
try:
    from reusable_theme_system import (get_theme_stylesheet, apply_theme_to_application, 
                                       get_available_themes, ThemeManager)
except ImportError:
    print("Theme system not found. Make sure reusable_theme_system directory is in Python path.")
    sys.exit(1)

class ExampleApplication(QMainWindow):
    """Example application using the reusable theme system."""
    
    def __init__(self):
        super().__init__()
        self.theme_manager = ThemeManager()
        self.init_ui()
        self.apply_theme("light")  # Start with light theme
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("RTB2000 Theme System - Example Application")
        self.setGeometry(200, 200, 900, 700)
        
        # Create toolbar
        self.create_toolbar()
        
        # Central widget with tabs
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Theme selector
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Select Theme:")
        theme_label.setProperty("class", "preset-label")
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems([theme.title() for theme in get_available_themes()])
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        main_layout.addLayout(theme_layout)
        
        # Tab widget
        tab_widget = QTabWidget()
        
        # Tab 1: Controls Demo
        controls_tab = self.create_controls_tab()
        tab_widget.addTab(controls_tab, "Controls Demo")
        
        # Tab 2: ScrollArea Demo
        scroll_tab = self.create_scroll_tab()
        tab_widget.addTab(scroll_tab, "ScrollArea Demo")
        
        # Tab 3: Interactive Demo
        interactive_tab = self.create_interactive_tab()
        tab_widget.addTab(interactive_tab, "Interactive Demo")
        
        main_layout.addWidget(tab_widget)
        
        # Status bar
        self.statusBar().showMessage("Ready - Professional theme system active")
        
    def create_toolbar(self):
        """Create application toolbar."""
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        
        # Various actions
        new_action = QAction("New", self)
        new_action.triggered.connect(lambda: self.statusBar().showMessage("New action triggered"))
        toolbar.addAction(new_action)
        
        open_action = QAction("Open", self)
        open_action.triggered.connect(lambda: self.statusBar().showMessage("Open action triggered"))
        toolbar.addAction(open_action)
        
        toolbar.addSeparator()
        
        save_action = QAction("Save", self)
        save_action.setCheckable(True)
        save_action.triggered.connect(lambda checked: self.statusBar().showMessage(f"Save: {'ON' if checked else 'OFF'}"))
        toolbar.addAction(save_action)
        
    def create_controls_tab(self):
        """Create controls demonstration tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Buttons group
        button_group = QGroupBox("Buttons & Actions")
        button_layout = QHBoxLayout(button_group)
        
        btn1 = QPushButton("Primary Button")
        btn2 = QPushButton("Secondary Button") 
        btn3 = QPushButton("Disabled Button")
        btn3.setEnabled(False)
        
        button_layout.addWidget(btn1)
        button_layout.addWidget(btn2)
        button_layout.addWidget(btn3)
        button_layout.addStretch()
        
        layout.addWidget(button_group)
        
        # Input controls group
        input_group = QGroupBox("Input Controls")
        input_layout = QVBoxLayout(input_group)
        
        # Text inputs
        text_row = QHBoxLayout()
        text_row.addWidget(QLabel("Text Input:"))
        line_edit = QLineEdit("Sample text")
        text_row.addWidget(line_edit)
        text_row.addStretch()
        input_layout.addLayout(text_row)
        
        # Number inputs
        number_row = QHBoxLayout()
        number_row.addWidget(QLabel("Number Input:"))
        spin_box = QSpinBox()
        spin_box.setValue(42)
        number_row.addWidget(spin_box)
        number_row.addStretch()
        input_layout.addLayout(number_row)
        
        # Combo box
        combo_row = QHBoxLayout()
        combo_row.addWidget(QLabel("Combo Box:"))
        combo_box = QComboBox()
        combo_box.addItems(["Option 1", "Option 2", "Option 3"])
        combo_row.addWidget(combo_box)
        combo_row.addStretch()
        input_layout.addLayout(combo_row)
        
        layout.addWidget(input_group)
        
        # Selection controls
        selection_group = QGroupBox("Selection Controls")
        selection_layout = QVBoxLayout(selection_group)
        
        # Checkboxes
        cb1 = QCheckBox("Enable feature A")
        cb2 = QCheckBox("Enable feature B")
        cb1.setChecked(True)
        
        # Radio buttons
        rb1 = QRadioButton("Option 1")
        rb2 = QRadioButton("Option 2")
        rb1.setChecked(True)
        
        selection_layout.addWidget(cb1)
        selection_layout.addWidget(cb2)
        selection_layout.addWidget(rb1)
        selection_layout.addWidget(rb2)
        
        layout.addWidget(selection_group)
        
        layout.addStretch()
        return widget
        
    def create_scroll_tab(self):
        """Create scroll area demonstration tab."""
        # Main widget
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        info_label = QLabel("ScrollArea with themed background and content:")
        info_label.setProperty("class", "status-label")
        layout.addWidget(info_label)
        
        # Scroll area
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Add many controls to test scrolling
        for i in range(20):
            group = QGroupBox(f"Group {i+1}")
            group_layout = QVBoxLayout(group)
            
            label = QLabel(f"This is item {i+1} in the scroll area")
            checkbox = QCheckBox(f"Enable item {i+1}")
            button = QPushButton(f"Action {i+1}")
            
            group_layout.addWidget(label)
            group_layout.addWidget(checkbox)
            group_layout.addWidget(button)
            
            scroll_layout.addWidget(group)
            
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        return widget
        
    def create_interactive_tab(self):
        """Create interactive demonstration tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Label types demo
        label_group = QGroupBox("Label Types")
        label_layout = QVBoxLayout(label_group)
        
        normal_label = QLabel("Normal Label")
        preset_label = QLabel("Preset Label")
        preset_label.setProperty("class", "preset-label")
        status_label = QLabel("Status: Connected")
        status_label.setProperty("class", "status-label")
        test_label = QLabel("Test: PASSED")
        test_label.setProperty("class", "test-label")
        
        label_layout.addWidget(normal_label)
        label_layout.addWidget(preset_label)
        label_layout.addWidget(status_label)
        label_layout.addWidget(test_label)
        
        layout.addWidget(label_group)
        
        # Slider demo
        slider_group = QGroupBox("Slider Control")
        slider_layout = QVBoxLayout(slider_group)
        
        slider_row = QHBoxLayout()
        slider_label = QLabel("Value:")
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(50)
        value_label = QLabel("50")
        
        slider.valueChanged.connect(lambda v: value_label.setText(str(v)))
        
        slider_row.addWidget(slider_label)
        slider_row.addWidget(slider)
        slider_row.addWidget(value_label)
        slider_layout.addLayout(slider_row)
        
        layout.addWidget(slider_group)
        
        # Interactive buttons
        action_group = QGroupBox("Theme Actions")
        action_layout = QHBoxLayout(action_group)
        
        light_btn = QPushButton("Switch to Light")
        dark_btn = QPushButton("Switch to Dark")
        
        light_btn.clicked.connect(lambda: self.apply_theme("light"))
        dark_btn.clicked.connect(lambda: self.apply_theme("dark"))
        
        action_layout.addWidget(light_btn)
        action_layout.addWidget(dark_btn)
        action_layout.addStretch()
        
        layout.addWidget(action_group)
        
        layout.addStretch()
        return widget
        
    def on_theme_changed(self, theme_text):
        """Handle theme combo box change."""
        theme_name = theme_text.lower()
        self.apply_theme(theme_name)
        
    def apply_theme(self, theme_name):
        """Apply the specified theme."""
        try:
            stylesheet = get_theme_stylesheet(theme_name)
            self.setStyleSheet(stylesheet)
            self.theme_combo.setCurrentText(theme_name.title())
            self.statusBar().showMessage(f"Applied {theme_name} theme successfully")
        except Exception as e:
            self.statusBar().showMessage(f"Error applying theme: {e}")

def main():
    """Main function."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Recommended for best theming results
    
    # Create and show the example application
    window = ExampleApplication()
    window.show()
    
    print("RTB2000 Theme System - Example Application")
    print("=" * 50)
    print("Features demonstrated:")
    print("- Light and Dark professional themes")
    print("- All Qt controls styled consistently")
    print("- Interactive theme switching")
    print("- ScrollArea background theming")
    print("- Professional button and input styling")
    print("- Label classes for different purposes")
    print("- ToolBar actions with hover effects")
    print("\nUse the theme selector or buttons to switch themes.")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
