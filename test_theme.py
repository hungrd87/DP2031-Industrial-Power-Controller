#!/usr/bin/env python3
"""
Quick theme test to verify theme switching
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QMenuBar, QToolBar, QLabel, QPushButton
from PyQt6.QtCore import Qt
from reusable_theme_system.theme_manager import get_theme_stylesheet

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.apply_theme("light")
        
    def setup_ui(self):
        self.setWindowTitle("Theme Test - DP2031")
        self.setGeometry(100, 100, 800, 600)
        
        # Menu Bar
        menubar = self.menuBar()
        view_menu = menubar.addMenu("View")
        
        # Theme switching actions
        light_action = view_menu.addAction("Light Theme")
        light_action.triggered.connect(lambda: self.apply_theme("light"))
        
        dark_action = view_menu.addAction("Dark Theme")  
        dark_action.triggered.connect(lambda: self.apply_theme("dark"))
        
        # Toolbar
        toolbar = self.addToolBar("Test Toolbar")
        toolbar.addAction("Test Action")
        toolbar.addSeparator()
        toolbar.addAction("Another Action")
        
        # Central Widget with TabWidget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # TabWidget test
        tab_widget = QTabWidget()
        
        # Tab 1
        tab1 = QWidget()
        tab1_layout = QVBoxLayout(tab1)
        tab1_layout.addWidget(QLabel("System Overview"))
        tab1_layout.addWidget(QPushButton("Test Button 1"))
        tab_widget.addTab(tab1, "System Overview")
        
        # Tab 2  
        tab2 = QWidget()
        tab2_layout = QVBoxLayout(tab2)
        tab2_layout.addWidget(QLabel("Channel Status"))
        tab2_layout.addWidget(QPushButton("Test Button 2"))
        tab_widget.addTab(tab2, "Channel Status")
        
        layout.addWidget(tab_widget)
        
    def apply_theme(self, theme_name):
        """Apply theme to the application"""
        stylesheet = get_theme_stylesheet(theme_name)
        
        app = QApplication.instance()
        if app:
            app.setStyleSheet(stylesheet)
            print(f"Applied {theme_name} theme")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())
