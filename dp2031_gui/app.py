"""
DP2031 Industrial Power Controller - Main Application

Professional PyQt6-based application for controlling RIGOL DP2000/DP2031
power supplies with industrial-style GUI and comprehensive monitoring.
"""

import sys
import os
import argparse
import signal
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# PyQt6 imports
try:
    from PyQt6.QtWidgets import QApplication, QMessageBox
    from PyQt6.QtCore import Qt, QTimer
    from PyQt6.QtGui import QIcon
except ImportError:
    print("ERROR: PyQt6 not found. Please install with: pip install PyQt6")
    sys.exit(1)

# Application imports
from .core.logging_cfg import setup_industrial_logging, get_logger
from .ui.main_window import MainWindow
from .core.dp2000_scpi import DP2000

import logging

# Application metadata
APP_NAME = "DP2031 Industrial Power Controller"
APP_VERSION = "1.0.0"
APP_ORGANIZATION = "Industrial Control Systems"
APP_DOMAIN = "instrumentcontrol.local"


class DP2031Application:
    """Main application class with initialization and lifecycle management."""
    
    def __init__(self):
        """Initialize application."""
        self.app = None
        self.main_window = None
        self.power_supply = None
        self.logger = None
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
    def _signal_handler(self, signum, frame):
        """Handle system signals for graceful shutdown."""
        if self.logger:
            self.logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.shutdown()
        sys.exit(0)
    
    def setup_logging(self, log_level: str = "INFO", log_dir: str = None) -> None:
        """Setup application logging."""
        try:
            root_logger, scpi_logger, measurement_logger = setup_industrial_logging()
            self.logger = logging.getLogger(__name__)
            
            self.logger.info(f"Starting {APP_NAME} v{APP_VERSION}")
            self.logger.info(f"Python version: {sys.version}")
            self.logger.info(f"Working directory: {os.getcwd()}")
            
        except Exception as e:
            print(f"ERROR: Failed to setup logging: {e}")
            sys.exit(1)
    
    def check_dependencies(self) -> bool:
        """Check that all required dependencies are available."""
        self.logger.info("Checking dependencies...")
        
        try:
            # Check PyQt6
            from PyQt6.QtCore import QT_VERSION_STR
            self.logger.info(f"PyQt6 version: {QT_VERSION_STR}")
            
            # Check NumPy
            import numpy
            self.logger.info(f"NumPy version: {numpy.__version__}")
            
            # Check pyqtgraph
            import pyqtgraph
            self.logger.info(f"pyqtgraph version: {pyqtgraph.__version__}")
            
            # Check PyVISA
            import pyvisa
            self.logger.info(f"PyVISA version: {pyvisa.__version__}")
            
            # Check VISA backends
            try:
                rm = pyvisa.ResourceManager()
                backends = rm.list_resources_info()
                self.logger.info(f"VISA backend available: {len(backends)} resources")
                rm.close()
            except Exception as e:
                self.logger.warning(f"VISA backend issue: {e}")
                self.logger.warning("Ensure NI-VISA or Keysight IO Libraries are installed")
            
            self.logger.info("All dependencies verified successfully")
            return True
            
        except ImportError as e:
            self.logger.error(f"Missing dependency: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Dependency check failed: {e}")
            return False
    
    def create_application(self) -> None:
        """Create QApplication with proper configuration."""
        self.logger.info("Creating Qt application...")
        
        # Create QApplication
        self.app = QApplication(sys.argv)
        
        # Set application properties
        self.app.setApplicationName(APP_NAME)
        self.app.setApplicationVersion(APP_VERSION)
        self.app.setOrganizationName(APP_ORGANIZATION)
        self.app.setOrganizationDomain(APP_DOMAIN)
        
        # Set application icon if available
        icon_path = project_root / "resources" / "dp2031_icon.png"
        if icon_path.exists():
            self.app.setWindowIcon(QIcon(str(icon_path)))
        
        # Setup application style for industrial look
        self.app.setStyleSheet("""
            QApplication {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 10pt;
            }
        """)
        
        self.logger.info("Qt application created successfully")
    
    def initialize_hardware(self) -> bool:
        """Initialize power supply connection (optional at startup)."""
        try:
            self.power_supply = DP2000()
            self.logger.info("Power supply driver initialized")
            return True
            
        except Exception as e:
            self.logger.warning(f"Power supply initialization failed: {e}")
            self.logger.info("Application will start without hardware connection")
            return False
    
    def create_main_window(self) -> None:
        """Create and setup main application window."""
        self.logger.info("Creating main window...")
        
        try:
            self.main_window = MainWindow()
            
            # Connect shutdown signal
            self.main_window.shutdown_requested.connect(self.shutdown)
            
            # Show window
            self.main_window.show()
            
            self.logger.info("Main window created and displayed")
            
        except Exception as e:
            self.logger.error(f"Failed to create main window: {e}")
            raise
    
    def setup_application_timer(self) -> None:
        """Setup periodic application tasks."""
        # Create timer for periodic tasks (status updates, etc.)
        self.app_timer = QTimer()
        self.app_timer.timeout.connect(self._periodic_tasks)
        self.app_timer.start(1000)  # Run every second
        
        self.logger.debug("Application timer started")
    
    def _periodic_tasks(self) -> None:
        """Periodic maintenance tasks."""
        # This can be used for periodic status checks, etc.
        pass
    
    def run(self) -> int:
        """Run the application main loop."""
        self.logger.info("Starting application main loop...")
        
        try:
            # Setup periodic tasks
            self.setup_application_timer()
            
            # Log startup completion
            self.logger.info("Application startup completed successfully")
            self.logger.info("Use File menu to connect to power supply")
            
            # Run Qt event loop
            result = self.app.exec()
            
            self.logger.info("Application event loop finished")
            return result
            
        except KeyboardInterrupt:
            self.logger.info("Application interrupted by user")
            return 0
        except Exception as e:
            self.logger.error(f"Application error: {e}", exc_info=True)
            return 1
    
    def shutdown(self) -> None:
        """Graceful application shutdown."""
        if self.logger:
            self.logger.info("Shutting down application...")
        
        try:
            # Close power supply connection
            if self.power_supply:
                self.power_supply.close()
            
            # Close main window
            if self.main_window:
                self.main_window.close()
            
            # Quit application
            if self.app:
                self.app.quit()
            
            if self.logger:
                self.logger.info("Application shutdown completed")
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error during shutdown: {e}")
    
    def show_error_dialog(self, title: str, message: str) -> None:
        """Show error dialog to user."""
        if self.app:
            QMessageBox.critical(None, title, message)
        else:
            print(f"ERROR: {title}: {message}")


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description=f"{APP_NAME} v{APP_VERSION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m dp2031_gui.app                    # Start application
  python -m dp2031_gui.app --debug            # Start with debug logging
  python -m dp2031_gui.app --resource USB0::  # Specify VISA resource pattern
        """
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"{APP_NAME} v{APP_VERSION}"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set logging level (default: INFO)"
    )
    
    parser.add_argument(
        "--log-dir",
        type=str,
        help="Directory for log files (default: ./logs)"
    )
    
    parser.add_argument(
        "--resource",
        type=str,
        help="Default VISA resource string or pattern"
    )
    
    parser.add_argument(
        "--no-splash",
        action="store_true",
        help="Disable splash screen"
    )
    
    return parser.parse_args()


def main() -> int:
    """Main application entry point."""
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Adjust log level for debug mode
    if args.debug:
        args.log_level = "DEBUG"
    
    # Create application instance
    app_instance = DP2031Application()
    
    try:
        # Setup logging
        app_instance.setup_logging(
            log_level=args.log_level,
            log_dir=args.log_dir
        )
        
        # Check dependencies
        if not app_instance.check_dependencies():
            app_instance.show_error_dialog(
                "Dependencies Error",
                "Required dependencies are missing. Please check the installation."
            )
            return 1
        
        # Create Qt application
        app_instance.create_application()
        
        # Initialize hardware (optional)
        app_instance.initialize_hardware()
        
        # Create main window
        app_instance.create_main_window()
        
        # Run application
        return app_instance.run()
        
    except Exception as e:
        error_msg = f"Failed to start application: {e}"
        if app_instance.logger:
            app_instance.logger.error(error_msg, exc_info=True)
        else:
            print(f"ERROR: {error_msg}")
        
        app_instance.show_error_dialog("Startup Error", error_msg)
        return 1
    
    finally:
        # Ensure cleanup
        app_instance.shutdown()


if __name__ == "__main__":
    sys.exit(main())
