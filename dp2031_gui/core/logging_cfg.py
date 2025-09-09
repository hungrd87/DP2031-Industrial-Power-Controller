"""
Logging Configuration for DP2031 Power Controller

Configures comprehensive logging for system events, SCPI commands,
measurements, and errors with appropriate formatting and file rotation.
"""

import logging
import logging.handlers
import os
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    log_level: str = "INFO",
    log_dir: Optional[str] = None,
    console_output: bool = True,
    file_output: bool = True,
    max_file_size: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 5
) -> logging.Logger:
    """
    Setup comprehensive logging for DP2031 application.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory for log files (default: ./logs)
        console_output: Enable console logging
        file_output: Enable file logging
        max_file_size: Maximum size per log file in bytes
        backup_count: Number of backup files to keep
        
    Returns:
        Configured root logger
    """
    
    # Create log directory
    if log_dir is None:
        log_dir = Path.cwd() / "logs"
    else:
        log_dir = Path(log_dir)
    
    log_dir.mkdir(exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        fmt='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)
    
    # File handlers
    if file_output:
        # Main application log
        app_log_file = log_dir / "dp2031_app.log"
        app_handler = logging.handlers.RotatingFileHandler(
            app_log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        app_handler.setLevel(logging.DEBUG)
        app_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(app_handler)
        
        # SCPI communication log (debug level)
        scpi_log_file = log_dir / "dp2031_scpi.log"
        scpi_handler = logging.handlers.RotatingFileHandler(
            scpi_log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        scpi_handler.setLevel(logging.DEBUG)
        scpi_handler.setFormatter(detailed_formatter)
        
        # Filter for SCPI-related logs
        scpi_filter = logging.Filter()
        scpi_filter.filter = lambda record: 'visa' in record.name.lower() or 'scpi' in record.name.lower()
        scpi_handler.addFilter(scpi_filter)
        root_logger.addHandler(scpi_handler)
        
        # Error log (warnings and above)
        error_log_file = log_dir / "dp2031_errors.log"
        error_handler = logging.handlers.RotatingFileHandler(
            error_log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.WARNING)
        error_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(error_handler)
    
    # Set specific logger levels
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('PyQt6').setLevel(logging.WARNING)
    
    # Log startup information
    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info("DP2031 Industrial Power Controller Starting")
    logger.info("=" * 60)
    logger.info(f"Log level: {log_level}")
    logger.info(f"Log directory: {log_dir}")
    logger.info(f"Console output: {console_output}")
    logger.info(f"File output: {file_output}")
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get logger for specific module.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


class SCPILogger:
    """Specialized logger for SCPI command tracking."""
    
    def __init__(self, logger_name: str = "scpi"):
        self.logger = logging.getLogger(logger_name)
        self.command_count = 0
        self.error_count = 0
        
    def log_command(self, command: str, response: Optional[str] = None, 
                   response_time: Optional[float] = None, error: Optional[str] = None):
        """
        Log SCPI command with response and timing.
        
        Args:
            command: SCPI command sent
            response: Response received (if any)
            response_time: Command execution time in seconds
            error: Error message (if any)
        """
        self.command_count += 1
        
        if error:
            self.error_count += 1
            self.logger.error(f"SCPI ERROR [{self.command_count}]: {command} -> {error}")
        else:
            timing_info = f" ({response_time:.3f}s)" if response_time else ""
            if response:
                self.logger.debug(f"SCPI [{self.command_count}]{timing_info}: {command} -> {response.strip()}")
            else:
                self.logger.debug(f"SCPI [{self.command_count}]{timing_info}: {command}")
    
    def get_statistics(self) -> dict:
        """Get SCPI logging statistics."""
        return {
            'total_commands': self.command_count,
            'error_count': self.error_count,
            'success_rate': (self.command_count - self.error_count) / max(1, self.command_count) * 100
        }


class MeasurementLogger:
    """Specialized logger for measurement data."""
    
    def __init__(self, log_dir: Optional[str] = None):
        self.logger = logging.getLogger("measurements")
        
        # Setup CSV data logging
        if log_dir is None:
            log_dir = Path.cwd() / "logs"
        else:
            log_dir = Path(log_dir)
        
        log_dir.mkdir(exist_ok=True)
        
        # Create data log file with timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.data_file = log_dir / f"dp2031_data_{timestamp}.csv"
        
        # Write CSV header
        header = "timestamp,channel,voltage,current,power,output_enabled,mode\n"
        with open(self.data_file, 'w', encoding='utf-8') as f:
            f.write(header)
        
        self.logger.info(f"Measurement logging started: {self.data_file}")
    
    def log_measurement(self, channel: int, voltage: float, current: float, 
                       power: float, output_enabled: bool, mode: str = ""):
        """
        Log measurement data to CSV file.
        
        Args:
            channel: Channel number
            voltage: Measured voltage
            current: Measured current
            power: Measured power
            output_enabled: Output state
            mode: Operating mode (CV/CC/UR)
        """
        import time
        timestamp = time.time()
        
        # Format data for CSV
        data_line = f"{timestamp:.3f},{channel},{voltage:.6f},{current:.6f},{power:.6f},{output_enabled},{mode}\n"
        
        try:
            with open(self.data_file, 'a', encoding='utf-8') as f:
                f.write(data_line)
        except Exception as e:
            self.logger.error(f"Failed to write measurement data: {e}")
    
    def create_snapshot(self, data: dict, filename: Optional[str] = None) -> str:
        """
        Create snapshot CSV file of current measurements.
        
        Args:
            data: Dictionary with measurement data
            filename: Optional filename (auto-generated if None)
            
        Returns:
            Path to created snapshot file
        """
        if filename is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dp2031_snapshot_{timestamp}.csv"
        
        log_dir = self.data_file.parent
        snapshot_file = log_dir / filename
        
        try:
            import csv
            with open(snapshot_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write headers
                writer.writerow(['Parameter', 'CH1', 'CH2', 'CH3'])
                
                # Write data rows
                for param in ['voltage', 'current', 'power']:
                    row = [param.capitalize()]
                    for ch in [1, 2, 3]:
                        value = data.get(f'ch{ch}_{param}', 'N/A')
                        row.append(value)
                    writer.writerow(row)
            
            self.logger.info(f"Snapshot created: {snapshot_file}")
            return str(snapshot_file)
            
        except Exception as e:
            self.logger.error(f"Failed to create snapshot: {e}")
            raise


def setup_industrial_logging() -> tuple[logging.Logger, SCPILogger, MeasurementLogger]:
    """
    Setup complete logging system for industrial application.
    
    Returns:
        Tuple of (root_logger, scpi_logger, measurement_logger)
    """
    # Setup main logging
    root_logger = setup_logging(
        log_level="INFO",
        console_output=True,
        file_output=True
    )
    
    # Setup specialized loggers
    scpi_logger = SCPILogger()
    measurement_logger = MeasurementLogger()
    
    logger = logging.getLogger(__name__)
    logger.info("Industrial logging system initialized")
    
    return root_logger, scpi_logger, measurement_logger


if __name__ == "__main__":
    # Test logging setup
    root_logger, scpi_logger, measurement_logger = setup_industrial_logging()
    
    logger = logging.getLogger("test")
    logger.info("Testing logging system")
    logger.warning("This is a warning")
    logger.error("This is an error")
    
    # Test SCPI logging
    scpi_logger.log_command("*IDN?", "RIGOL TECHNOLOGIES,DP2031,DP2D251800001,00.01.14", 0.045)
    scpi_logger.log_command(":OUTP1 ON", None, 0.012)
    scpi_logger.log_command(":MEAS:ALL? CH1", "5.000,1.000,5.000", 0.025)
    
    # Test measurement logging
    measurement_logger.log_measurement(1, 5.0, 1.0, 5.0, True, "CV")
    
    print("Logging test completed. Check logs/ directory for output files.")
