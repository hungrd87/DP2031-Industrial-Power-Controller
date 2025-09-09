"""
VISA Session Management for DP2031 Power Controller

Handles low-level VISA communication with automatic reconnection,
error handling, and optimized settings for RIGOL DP2000/DP2031.
"""

import time
import logging
from typing import Optional, Any, Union
from contextlib import contextmanager

try:
    import pyvisa
    from pyvisa import ResourceManager, VisaIOError
    VISA_AVAILABLE = True
except ImportError:
    VISA_AVAILABLE = False
    ResourceManager = None
    VisaIOError = Exception

logger = logging.getLogger(__name__)


class VISAError(Exception):
    """Custom exception for VISA-related errors."""
    pass


class VISASession:
    """
    VISA Session Manager for RIGOL DP2000/DP2031 Power Supplies.
    
    Provides robust communication with automatic reconnection, error handling,
    and optimized settings for industrial applications.
    """
    
    def __init__(self):
        """Initialize VISA session manager."""
        if not VISA_AVAILABLE:
            raise VISAError("PyVISA not available. Install with: pip install pyvisa")
        
        self.resource_manager: Optional[ResourceManager] = None
        self.instrument: Optional[Any] = None
        self.resource_string: Optional[str] = None
        self.is_connected: bool = False
        
        # Connection settings
        self.timeout_ms: int = 5000  # 5 seconds
        self.read_termination: str = '\n'
        self.write_termination: str = '\n'
        self.encoding: str = 'utf-8'
        
        # Retry settings
        self.max_retries: int = 2
        self.retry_delay: float = 0.1  # seconds
        
        # Statistics
        self.command_count: int = 0
        self.error_count: int = 0
        self.last_error: Optional[str] = None
        self.connection_time: Optional[float] = None
        
    def __enter__(self):
        """Context manager entry."""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensure cleanup."""
        self.close()
        
    def initialize_visa(self) -> None:
        """Initialize VISA resource manager."""
        try:
            if self.resource_manager is None:
                self.resource_manager = pyvisa.ResourceManager()
                logger.info("VISA Resource Manager initialized")
        except Exception as e:
            raise VISAError(f"Failed to initialize VISA: {e}")
    
    def list_resources(self) -> list[str]:
        """
        List available VISA resources.
        
        Returns:
            List of resource strings
        """
        self.initialize_visa()
        try:
            resources = self.resource_manager.list_resources()
            logger.info(f"Found {len(resources)} VISA resources: {list(resources)}")
            return list(resources)
        except Exception as e:
            logger.warning(f"Failed to list resources: {e}")
            return []
    
    def connect(self, resource_string: str, **kwargs) -> None:
        """
        Connect to VISA instrument.
        
        Args:
            resource_string: VISA resource identifier
            **kwargs: Additional connection parameters
        """
        if self.is_connected:
            logger.warning("Already connected, disconnecting first")
            self.disconnect()
        
        self.initialize_visa()
        self.resource_string = resource_string
        
        try:
            start_time = time.time()
            
            # Open instrument connection
            self.instrument = self.resource_manager.open_resource(resource_string)
            
            # Configure communication settings
            self.instrument.timeout = kwargs.get('timeout', self.timeout_ms)
            self.instrument.read_termination = kwargs.get('read_termination', self.read_termination)
            self.instrument.write_termination = kwargs.get('write_termination', self.write_termination)
            self.instrument.encoding = kwargs.get('encoding', self.encoding)
            
            # Test connection with identification query
            idn = self.query("*IDN?", timeout=3000)
            
            self.connection_time = time.time() - start_time
            self.is_connected = True
            self.error_count = 0
            self.last_error = None
            
            logger.info(f"Connected to {resource_string} in {self.connection_time:.3f}s")
            logger.info(f"Instrument ID: {idn.strip()}")
            
        except Exception as e:
            self.last_error = str(e)
            self.error_count += 1
            logger.error(f"Failed to connect to {resource_string}: {e}")
            raise VISAError(f"Connection failed: {e}")
    
    def disconnect(self) -> None:
        """Disconnect from instrument."""
        if self.instrument:
            try:
                self.instrument.close()
                logger.info("Instrument connection closed")
            except Exception as e:
                logger.warning(f"Error closing instrument: {e}")
            finally:
                self.instrument = None
                self.is_connected = False
    
    def close(self) -> None:
        """Close VISA session and cleanup resources."""
        self.disconnect()
        
        if self.resource_manager:
            try:
                self.resource_manager.close()
                logger.info("VISA Resource Manager closed")
            except Exception as e:
                logger.warning(f"Error closing resource manager: {e}")
            finally:
                self.resource_manager = None
    
    def write(self, command: str, **kwargs) -> None:
        """
        Write command to instrument.
        
        Args:
            command: SCPI command string
            **kwargs: Additional write parameters
        """
        if not self.is_connected or not self.instrument:
            raise VISAError("Not connected to instrument")
        
        for attempt in range(self.max_retries + 1):
            try:
                start_time = time.time()
                bytes_written = self.instrument.write(command)
                response_time = time.time() - start_time
                
                self.command_count += 1
                logger.debug(f"WRITE [{response_time:.3f}s]: {command} ({bytes_written} bytes)")
                return
                
            except VisaIOError as e:
                if attempt < self.max_retries:
                    logger.warning(f"Write attempt {attempt + 1} failed, retrying: {e}")
                    time.sleep(self.retry_delay)
                    continue
                else:
                    self.error_count += 1
                    self.last_error = str(e)
                    logger.error(f"Write failed after {self.max_retries} retries: {e}")
                    raise VISAError(f"Write failed: {e}")
    
    def read(self, **kwargs) -> str:
        """
        Read response from instrument.
        
        Returns:
            Response string
        """
        if not self.is_connected or not self.instrument:
            raise VISAError("Not connected to instrument")
        
        for attempt in range(self.max_retries + 1):
            try:
                start_time = time.time()
                response = self.instrument.read()
                response_time = time.time() - start_time
                
                logger.debug(f"READ [{response_time:.3f}s]: {response.strip()} ({len(response)} chars)")
                return response
                
            except VisaIOError as e:
                if attempt < self.max_retries:
                    logger.warning(f"Read attempt {attempt + 1} failed, retrying: {e}")
                    time.sleep(self.retry_delay)
                    continue
                else:
                    self.error_count += 1
                    self.last_error = str(e)
                    logger.error(f"Read failed after {self.max_retries} retries: {e}")
                    raise VISAError(f"Read failed: {e}")
    
    def query(self, command: str, timeout: Optional[int] = None) -> str:
        """
        Write command and read response.
        
        Args:
            command: SCPI command string
            timeout: Optional timeout override in milliseconds
            
        Returns:
            Response string
        """
        if not self.is_connected or not self.instrument:
            raise VISAError("Not connected to instrument")
        
        # Save and set timeout if specified
        original_timeout = None
        if timeout is not None:
            original_timeout = self.instrument.timeout
            self.instrument.timeout = timeout
        
        try:
            for attempt in range(self.max_retries + 1):
                try:
                    start_time = time.time()
                    response = self.instrument.query(command)
                    response_time = time.time() - start_time
                    
                    self.command_count += 1
                    logger.debug(f"QUERY [{response_time:.3f}s]: {command} -> {response.strip()}")
                    return response
                    
                except VisaIOError as e:
                    if attempt < self.max_retries:
                        logger.warning(f"Query attempt {attempt + 1} failed, retrying: {e}")
                        time.sleep(self.retry_delay)
                        continue
                    else:
                        self.error_count += 1
                        self.last_error = str(e)
                        logger.error(f"Query failed after {self.max_retries} retries: {e}")
                        raise VISAError(f"Query failed: {e}")
        finally:
            # Restore original timeout
            if original_timeout is not None:
                self.instrument.timeout = original_timeout
    
    def check_connection(self) -> bool:
        """
        Check if connection is still active.
        
        Returns:
            True if connection is active
        """
        if not self.is_connected or not self.instrument:
            return False
        
        try:
            # Quick identification query to test connection
            self.query("*IDN?", timeout=1000)
            return True
        except Exception as e:
            logger.warning(f"Connection check failed: {e}")
            self.is_connected = False
            return False
    
    def auto_reconnect(self) -> bool:
        """
        Attempt automatic reconnection.
        
        Returns:
            True if reconnection successful
        """
        if not self.resource_string:
            logger.error("No resource string available for reconnection")
            return False
        
        logger.info(f"Attempting reconnection to {self.resource_string}")
        
        try:
            self.disconnect()
            time.sleep(1.0)  # Wait before reconnection
            self.connect(self.resource_string)
            logger.info("Automatic reconnection successful")
            return True
        except Exception as e:
            logger.error(f"Automatic reconnection failed: {e}")
            return False
    
    @contextmanager
    def error_recovery(self):
        """Context manager for automatic error recovery."""
        try:
            yield
        except VISAError as e:
            logger.warning(f"VISA error detected: {e}")
            if self.auto_reconnect():
                logger.info("Recovered from VISA error via reconnection")
            else:
                raise
    
    def get_statistics(self) -> dict:
        """
        Get connection statistics.
        
        Returns:
            Dictionary with statistics
        """
        return {
            'connected': self.is_connected,
            'resource': self.resource_string,
            'command_count': self.command_count,
            'error_count': self.error_count,
            'last_error': self.last_error,
            'connection_time': self.connection_time,
            'timeout_ms': self.timeout_ms if self.instrument else None,
        }
    
    def __repr__(self) -> str:
        """String representation."""
        status = "connected" if self.is_connected else "disconnected"
        return f"VISASession({self.resource_string}, {status})"
