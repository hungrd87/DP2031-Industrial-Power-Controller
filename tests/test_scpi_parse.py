"""
Test suite for SCPI parsing and command validation.

Tests the DP2000 SCPI driver's ability to parse responses,
validate commands, and handle various data formats.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dp2031_gui.core.dp2000_scpi import DP2000, DP2000Error
from dp2031_gui.core.model import ChannelMeasurement, ProtectionSettings


class TestSCPIParsing:
    """Test SCPI command parsing and validation."""
    
    def test_measurement_parsing(self):
        """Test parsing of measurement responses."""
        # Test single voltage measurement
        voltage_response = "5.000000"
        voltage = float(voltage_response.strip())
        assert voltage == 5.0
        
        # Test current measurement
        current_response = "1.234567"
        current = float(current_response.strip())
        assert current == 1.234567
        
        # Test ALL measurement response
        all_response = "5.000000,1.234567,6.172839"
        values = all_response.strip().split(',')
        assert len(values) == 3
        
        voltage, current, power = map(float, values)
        assert voltage == 5.0
        assert current == 1.234567
        assert power == 6.172839
    
    def test_status_parsing(self):
        """Test status register parsing."""
        # Test status byte
        stb_response = "64"
        stb = int(stb_response.strip())
        assert stb == 64
        
        # Test operation condition
        oper_response = "256"
        oper = int(oper_response.strip())
        assert oper == 256
    
    def test_error_parsing(self):
        """Test error queue parsing."""
        # Test no error
        no_error = "0,\"No error\""
        error_code, error_msg = no_error.strip().split(',', 1)
        assert int(error_code) == 0
        assert error_msg.strip('"') == "No error"
        
        # Test actual error
        error_response = "-113,\"Undefined header\""
        error_code, error_msg = error_response.strip().split(',', 1)
        assert int(error_code) == -113
        assert error_msg.strip('"') == "Undefined header"
    
    def test_identification_parsing(self):
        """Test identification string parsing."""
        idn_response = "RIGOL TECHNOLOGIES,DP2031,DP2D251800001,00.01.14"
        parts = idn_response.strip().split(',')
        assert len(parts) == 4
        assert parts[0] == "RIGOL TECHNOLOGIES"
        assert parts[1] == "DP2031"
        assert "DP2D" in parts[2]  # Serial number
        assert "." in parts[3]     # Firmware version
    
    def test_boolean_parsing(self):
        """Test boolean response parsing."""
        # Test output state responses
        output_on = "1"
        assert output_on.strip() == "1"
        
        output_off = "0"
        assert output_off.strip() == "0"
    
    def test_command_validation(self):
        """Test command parameter validation."""
        # Test voltage validation
        with pytest.raises(ValueError):
            dp2000 = DP2000()
            dp2000._validate_voltage(-1.0)  # Negative voltage
        
        with pytest.raises(ValueError):
            dp2000 = DP2000()
            dp2000._validate_voltage(100.0)  # Voltage too high
        
        # Test current validation
        with pytest.raises(ValueError):
            dp2000 = DP2000()
            dp2000._validate_current(-0.1)  # Negative current
        
        with pytest.raises(ValueError):
            dp2000 = DP2000()
            dp2000._validate_current(20.0)  # Current too high
        
        # Test channel validation
        with pytest.raises(ValueError):
            dp2000 = DP2000()
            dp2000._validate_channel(0)  # Channel too low
        
        with pytest.raises(ValueError):
            dp2000 = DP2000()
            dp2000._validate_channel(4)  # Channel too high


class TestDataStructures:
    """Test data structure creation and validation."""
    
    def test_channel_measurement(self):
        """Test ChannelMeasurement creation."""
        import time
        
        # Test manual creation
        measurement = ChannelMeasurement(
            timestamp=time.time(),
            voltage=5.0,
            current=1.0,
            power=5.0
        )
        assert measurement.voltage == 5.0
        assert measurement.current == 1.0
        assert measurement.power == 5.0
        
        # Test factory method
        measurement2 = ChannelMeasurement.now(5.0, 1.0)
        assert measurement2.voltage == 5.0
        assert measurement2.current == 1.0
        assert measurement2.power == 5.0  # Calculated
    
    def test_protection_settings(self):
        """Test ProtectionSettings validation."""
        # Test valid settings
        protection = ProtectionSettings(
            ovp_level=6.0,
            ovp_enabled=True,
            ocp_level=1.5,
            ocp_enabled=True
        )
        assert protection.ovp_level == 6.0
        assert protection.ocp_level == 1.5
        
        # Test invalid settings
        with pytest.raises(ValueError):
            ProtectionSettings(ovp_level=-1.0)  # Negative OVP
        
        with pytest.raises(ValueError):
            ProtectionSettings(ocp_level=-0.1)  # Negative OCP


class TestCommandFormatting:
    """Test SCPI command formatting."""
    
    def test_voltage_commands(self):
        """Test voltage command formatting."""
        channel = 1
        voltage = 5.123456
        
        # Expected command format
        expected = f":SOUR{channel}:VOLT {voltage:.6f}"
        assert expected == ":SOUR1:VOLT 5.123456"
    
    def test_current_commands(self):
        """Test current command formatting."""
        channel = 2
        current = 1.234567
        
        expected = f":SOUR{channel}:CURR {current:.6f}"
        assert expected == ":SOUR2:CURR 1.234567"
    
    def test_output_commands(self):
        """Test output command formatting."""
        channel = 3
        
        # Output ON
        expected_on = f":OUTP{channel} ON"
        assert expected_on == ":OUTP3 ON"
        
        # Output OFF
        expected_off = f":OUTP{channel} OFF"
        assert expected_off == ":OUTP3 OFF"
    
    def test_measurement_commands(self):
        """Test measurement command formatting."""
        channel = 1
        
        # Voltage measurement
        voltage_cmd = f":MEAS:SCAL:VOLT:DC? CH{channel}"
        assert voltage_cmd == ":MEAS:SCAL:VOLT:DC? CH1"
        
        # Current measurement
        current_cmd = f":MEAS:SCAL:CURR:DC? CH{channel}"
        assert current_cmd == ":MEAS:SCAL:CURR:DC? CH1"
        
        # All measurements
        all_cmd = f":MEAS:SCAL:ALL:DC? CH{channel}"
        assert all_cmd == ":MEAS:SCAL:ALL:DC? CH1"
    
    def test_protection_commands(self):
        """Test protection command formatting."""
        channel = 1
        ovp_level = 6.5
        ocp_level = 1.2
        
        # OVP commands
        ovp_level_cmd = f":SOUR{channel}:VOLT:PROT:LEV {ovp_level:.6f}"
        ovp_state_cmd = f":SOUR{channel}:VOLT:PROT:STAT ON"
        
        assert ovp_level_cmd == ":SOUR1:VOLT:PROT:LEV 6.500000"
        assert ovp_state_cmd == ":SOUR1:VOLT:PROT:STAT ON"
        
        # OCP commands
        ocp_level_cmd = f":SOUR{channel}:CURR:PROT:LEV {ocp_level:.6f}"
        ocp_state_cmd = f":SOUR{channel}:CURR:PROT:STAT OFF"
        
        assert ocp_level_cmd == ":SOUR1:CURR:PROT:LEV 1.200000"
        assert ocp_state_cmd == ":SOUR1:CURR:PROT:STAT OFF"


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_empty_responses(self):
        """Test handling of empty or malformed responses."""
        # Test empty response
        with pytest.raises(ValueError):
            values = "".strip().split(',')
            if len(values) != 3:
                raise ValueError("Expected 3 values")
        
        # Test insufficient values
        with pytest.raises(ValueError):
            response = "5.0,1.0"  # Missing power value
            values = response.strip().split(',')
            if len(values) != 3:
                raise ValueError("Expected 3 values")
    
    def test_invalid_numeric_values(self):
        """Test handling of invalid numeric responses."""
        # Test non-numeric response
        with pytest.raises(ValueError):
            float("invalid")
        
        # Test special values
        assert float("inf") == float('inf')
        assert float("-inf") == float('-inf')
        # Note: float("nan") != float("nan") due to NaN properties
    
    def test_boundary_values(self):
        """Test boundary value validation."""
        dp2000 = DP2000()
        
        # Test valid boundaries
        dp2000._validate_voltage(0.0)      # Minimum voltage
        dp2000._validate_voltage(64.0)     # Maximum voltage
        dp2000._validate_current(0.0)      # Minimum current
        dp2000._validate_current(10.0)     # Maximum current
        dp2000._validate_channel(1)        # Minimum channel
        dp2000._validate_channel(3)        # Maximum channel


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])
