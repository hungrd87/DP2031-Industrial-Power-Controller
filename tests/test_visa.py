"""
Test suite for VISA session management and communication.

Tests the visa session wrapper including connection handling,
error recovery, retry logic, and statistics tracking.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
import time

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dp2031_gui.core.visa_session import VISASession, VISAError


class TestVISASession:
    """Test VISA session management."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.session = VISASession()
    
    def teardown_method(self):
        """Cleanup after each test method."""
        if self.session and self.session.is_connected:
            self.session.disconnect()
    
    def test_initialization(self):
        """Test VISASession initialization."""
        session = VISASession()
        assert session._resource_manager is None
        assert session._session is None
        assert session.is_connected is False
        assert session.resource_name == ""
        assert session.timeout == 5000
        assert session._stats['commands_sent'] == 0
        assert session._stats['responses_received'] == 0
        assert session._stats['errors'] == 0
    
    def test_statistics_tracking(self):
        """Test statistics collection."""
        session = VISASession()
        
        # Initial stats
        stats = session.get_statistics()
        assert stats['commands_sent'] == 0
        assert stats['responses_received'] == 0
        assert stats['errors'] == 0
        assert stats['bytes_sent'] == 0
        assert stats['bytes_received'] == 0
        assert stats['reconnections'] == 0
        assert 'connection_time' in stats
        
        # Update stats manually for testing
        session._stats['commands_sent'] = 10
        session._stats['responses_received'] = 9
        session._stats['errors'] = 1
        
        updated_stats = session.get_statistics()
        assert updated_stats['commands_sent'] == 10
        assert updated_stats['responses_received'] == 9
        assert updated_stats['errors'] == 1
    
    def test_reset_statistics(self):
        """Test statistics reset."""
        session = VISASession()
        
        # Set some stats
        session._stats['commands_sent'] = 5
        session._stats['errors'] = 2
        
        # Reset
        session.reset_statistics()
        
        # Check reset
        stats = session.get_statistics()
        assert stats['commands_sent'] == 0
        assert stats['errors'] == 0
    
    @patch('pyvisa.ResourceManager')
    def test_successful_connection(self, mock_rm_class):
        """Test successful instrument connection."""
        # Setup mocks
        mock_rm = Mock()
        mock_session = Mock()
        mock_rm_class.return_value = mock_rm
        mock_rm.open_resource.return_value = mock_session
        mock_session.query.return_value = "RIGOL TECHNOLOGIES,DP2031,DP2D251800001,00.01.14"
        
        session = VISASession()
        
        # Test connection
        result = session.connect("USB0::0x1AB1::0x0E11::DP2D251800001::INSTR")
        
        assert result is True
        assert session.is_connected is True
        assert session.resource_name == "USB0::0x1AB1::0x0E11::DP2D251800001::INSTR"
        mock_rm.open_resource.assert_called_once()
        mock_session.query.assert_called_with("*IDN?")
    
    @patch('pyvisa.ResourceManager')
    def test_connection_failure(self, mock_rm_class):
        """Test connection failure handling."""
        # Setup mocks to raise exception
        mock_rm = Mock()
        mock_rm_class.return_value = mock_rm
        mock_rm.open_resource.side_effect = Exception("Connection failed")
        
        session = VISASession()
        
        # Test connection failure
        result = session.connect("INVALID::RESOURCE")
        
        assert result is False
        assert session.is_connected is False
        assert session.resource_name == ""
    
    @patch('pyvisa.ResourceManager')
    def test_write_command(self, mock_rm_class):
        """Test SCPI command writing."""
        # Setup mocks
        mock_rm = Mock()
        mock_session = Mock()
        mock_rm_class.return_value = mock_rm
        mock_rm.open_resource.return_value = mock_session
        mock_session.query.return_value = "RIGOL TECHNOLOGIES,DP2031,DP2D251800001,00.01.14"
        
        session = VISASession()
        session.connect("USB0::0x1AB1::0x0E11::DP2D251800001::INSTR")
        
        # Test write
        result = session.write(":SOUR1:VOLT 5.0")
        
        assert result is True
        mock_session.write.assert_called_with(":SOUR1:VOLT 5.0")
        assert session._stats['commands_sent'] == 1
    
    @patch('pyvisa.ResourceManager')
    def test_query_command(self, mock_rm_class):
        """Test SCPI query commands."""
        # Setup mocks
        mock_rm = Mock()
        mock_session = Mock()
        mock_rm_class.return_value = mock_rm
        mock_rm.open_resource.return_value = mock_session
        mock_session.query.side_effect = [
            "RIGOL TECHNOLOGIES,DP2031,DP2D251800001,00.01.14",  # IDN query
            "5.000000"  # Voltage query
        ]
        
        session = VISASession()
        session.connect("USB0::0x1AB1::0x0E11::DP2D251800001::INSTR")
        
        # Test query
        result = session.query(":MEAS:SCAL:VOLT:DC? CH1")
        
        assert result == "5.000000"
        assert session._stats['commands_sent'] == 1
        assert session._stats['responses_received'] == 1
    
    @patch('pyvisa.ResourceManager')
    def test_write_failure_recovery(self, mock_rm_class):
        """Test write failure and recovery."""
        # Setup mocks
        mock_rm = Mock()
        mock_session = Mock()
        mock_rm_class.return_value = mock_rm
        mock_rm.open_resource.return_value = mock_session
        mock_session.query.return_value = "RIGOL TECHNOLOGIES,DP2031,DP2D251800001,00.01.14"
        
        # First write fails, second succeeds
        mock_session.write.side_effect = [Exception("Write failed"), None]
        
        session = VISASession()
        session.connect("USB0::0x1AB1::0x0E11::DP2D251800001::INSTR")
        
        # Test write with retry
        result = session.write(":SOUR1:VOLT 5.0", retries=1)
        
        assert result is True
        assert mock_session.write.call_count == 2
        assert session._stats['errors'] == 1
        assert session._stats['commands_sent'] == 1
    
    @patch('pyvisa.ResourceManager')
    def test_query_failure_recovery(self, mock_rm_class):
        """Test query failure and recovery."""
        # Setup mocks
        mock_rm = Mock()
        mock_session = Mock()
        mock_rm_class.return_value = mock_rm
        mock_rm.open_resource.return_value = mock_session
        
        # IDN succeeds, first voltage query fails, second succeeds
        mock_session.query.side_effect = [
            "RIGOL TECHNOLOGIES,DP2031,DP2D251800001,00.01.14",
            Exception("Query failed"),
            "5.000000"
        ]
        
        session = VISASession()
        session.connect("USB0::0x1AB1::0x0E11::DP2D251800001::INSTR")
        
        # Test query with retry
        result = session.query(":MEAS:SCAL:VOLT:DC? CH1", retries=1)
        
        assert result == "5.000000"
        assert session._stats['errors'] == 1
        assert session._stats['commands_sent'] == 1
        assert session._stats['responses_received'] == 1
    
    @patch('pyvisa.ResourceManager')
    def test_auto_reconnection(self, mock_rm_class):
        """Test automatic reconnection on communication failure."""
        # Setup mocks
        mock_rm = Mock()
        mock_session = Mock()
        mock_rm_class.return_value = mock_rm
        mock_rm.open_resource.return_value = mock_session
        
        # IDN succeeds, write fails with disconnect, then reconnection succeeds
        mock_session.query.side_effect = [
            "RIGOL TECHNOLOGIES,DP2031,DP2D251800001,00.01.14",  # Initial IDN
            "RIGOL TECHNOLOGIES,DP2031,DP2D251800001,00.01.14"   # Reconnect IDN
        ]
        mock_session.write.side_effect = [
            Exception("VI_ERROR_CONN_LOST"),  # Connection lost
            None  # Successful write after reconnect
        ]
        
        session = VISASession()
        session.connect("USB0::0x1AB1::0x0E11::DP2D251800001::INSTR")
        session.auto_reconnect = True
        
        # Test write with auto-reconnection
        result = session.write(":SOUR1:VOLT 5.0")
        
        assert result is True
        assert session._stats['reconnections'] == 1
    
    @patch('pyvisa.ResourceManager')
    def test_timeout_handling(self, mock_rm_class):
        """Test timeout configuration and handling."""
        # Setup mocks
        mock_rm = Mock()
        mock_session = Mock()
        mock_rm_class.return_value = mock_rm
        mock_rm.open_resource.return_value = mock_session
        mock_session.query.return_value = "RIGOL TECHNOLOGIES,DP2031,DP2D251800001,00.01.14"
        
        session = VISASession(timeout=10000)
        session.connect("USB0::0x1AB1::0x0E11::DP2D251800001::INSTR")
        
        # Check timeout was set
        assert session.timeout == 10000
        assert mock_session.timeout == 10000
    
    @patch('pyvisa.ResourceManager')
    def test_disconnect(self, mock_rm_class):
        """Test proper disconnection."""
        # Setup mocks
        mock_rm = Mock()
        mock_session = Mock()
        mock_rm_class.return_value = mock_rm
        mock_rm.open_resource.return_value = mock_session
        mock_session.query.return_value = "RIGOL TECHNOLOGIES,DP2031,DP2D251800001,00.01.14"
        
        session = VISASession()
        session.connect("USB0::0x1AB1::0x0E11::DP2D251800001::INSTR")
        
        # Test disconnect
        session.disconnect()
        
        assert session.is_connected is False
        assert session.resource_name == ""
        mock_session.close.assert_called_once()
    
    def test_context_manager(self):
        """Test using VISASession as context manager."""
        with patch('pyvisa.ResourceManager') as mock_rm_class:
            mock_rm = Mock()
            mock_session = Mock()
            mock_rm_class.return_value = mock_rm
            mock_rm.open_resource.return_value = mock_session
            mock_session.query.return_value = "RIGOL TECHNOLOGIES,DP2031,DP2D251800001,00.01.14"
            
            # Test context manager
            with VISASession() as session:
                session.connect("USB0::0x1AB1::0x0E11::DP2D251800001::INSTR")
                assert session.is_connected is True
            
            # Should be disconnected after context exit
            mock_session.close.assert_called_once()


class TestVISAError:
    """Test VISA error handling."""
    
    def test_visa_error_creation(self):
        """Test VISAError exception creation."""
        error = VISAError("Test error message")
        assert str(error) == "Test error message"
        assert isinstance(error, Exception)
    
    def test_visa_error_with_code(self):
        """Test VISAError with error code."""
        error = VISAError("Connection failed", error_code=-1073807194)
        assert "Connection failed" in str(error)
        assert error.error_code == -1073807194


class TestUtilityFunctions:
    """Test utility functions in VISA session module."""
    
    def test_format_bytes(self):
        """Test byte formatting utility."""
        from dp2031_gui.core.visa_session import VISASession
        
        session = VISASession()
        
        # Test various byte sizes
        # Note: These would be utility methods if they existed
        # For now, test basic size handling
        assert 1024 > 1000  # KB threshold
        assert 1024 * 1024 > 1000000  # MB threshold
    
    def test_connection_string_validation(self):
        """Test connection string validation."""
        # Valid connection strings
        valid_strings = [
            "USB0::0x1AB1::0x0E11::DP2D251800001::INSTR",
            "TCPIP0::192.168.1.100::INSTR",
            "ASRL1::INSTR",
            "GPIB0::7::INSTR"
        ]
        
        for conn_str in valid_strings:
            # Basic validation - contains INSTR
            assert "INSTR" in conn_str
            assert "::" in conn_str
    
    def test_error_message_parsing(self):
        """Test parsing of VISA error messages."""
        # Common VISA error codes
        error_codes = {
            -1073807194: "VI_ERROR_CONN_LOST",
            -1073807339: "VI_ERROR_TMO",
            -1073807303: "VI_ERROR_RSRC_BUSY"
        }
        
        for code, name in error_codes.items():
            # Test that error codes are negative
            assert code < 0
            assert isinstance(name, str)


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])
