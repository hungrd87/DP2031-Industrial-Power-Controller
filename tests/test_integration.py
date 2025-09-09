"""
Integration tests for DP2031 Industrial Power Controller.

Tests the complete integration between VISA session, SCPI driver,
and data models in realistic scenarios.
"""

import pytest
import sys
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dp2031_gui.core.visa_session import VISASession
from dp2031_gui.core.dp2000_scpi import DP2000
from dp2031_gui.core.model import ChannelMeasurement, ProtectionSettings


@pytest.mark.integration
class TestDP2031Integration:
    """Integration tests for complete system."""
    
    @patch('pyvisa.ResourceManager')
    def test_complete_measurement_cycle(self, mock_rm_class):
        """Test complete measurement cycle from connection to data."""
        # Setup comprehensive mock
        mock_rm = Mock()
        mock_session = Mock()
        mock_rm_class.return_value = mock_rm
        mock_rm.open_resource.return_value = mock_session
        
        # Configure realistic responses
        mock_session.query.side_effect = [
            "RIGOL TECHNOLOGIES,DP2031,DP2D251800001,00.01.14",  # IDN
            "5.000000,1.000000,5.000000",  # ALL measurement CH1
            "3.300000,0.500000,1.650000",  # ALL measurement CH2
            "12.000000,0.200000,2.400000"  # ALL measurement CH3
        ]
        
        # Create integrated system
        dp2000 = DP2000()
        
        # Test connection
        connected = dp2000.connect("USB0::0x1AB1::0x0E11::DP2D251800001::INSTR")
        assert connected is True
        
        # Test measurements for all channels
        measurements = {}
        for channel in [1, 2, 3]:
            meas = dp2000.measure_all(channel)
            measurements[channel] = meas
            
            # Verify measurement structure
            assert isinstance(meas, ChannelMeasurement)
            assert meas.voltage > 0
            assert meas.current >= 0
            assert meas.power >= 0
        
        # Verify different values per channel
        assert measurements[1].voltage != measurements[2].voltage
        assert measurements[2].voltage != measurements[3].voltage
        
        # Test disconnection
        dp2000.disconnect()
        assert dp2000.is_connected is False
    
    @patch('pyvisa.ResourceManager')
    def test_power_supply_control_sequence(self, mock_rm_class):
        """Test complete power supply control sequence."""
        # Setup mock
        mock_rm = Mock()
        mock_session = Mock()
        mock_rm_class.return_value = mock_rm
        mock_rm.open_resource.return_value = mock_session
        
        # Configure responses
        mock_session.query.side_effect = [
            "RIGOL TECHNOLOGIES,DP2031,DP2D251800001,00.01.14",  # IDN
            "0",  # Initial output state (OFF)
            "1",  # Output state after enable (ON)
            "5.000000",  # Voltage readback
            "1.500000",  # Current readback
            "0"   # Final output state (OFF)
        ]
        
        dp2000 = DP2000()
        dp2000.connect("USB0::0x1AB1::0x0E11::DP2D251800001::INSTR")
        
        channel = 1
        
        # 1. Verify initial state
        initial_state = dp2000.get_output_state(channel)
        assert initial_state is False
        
        # 2. Set voltage and current
        dp2000.set_voltage(channel, 5.0)
        dp2000.set_current(channel, 1.5)
        
        # 3. Enable output
        dp2000.set_output_state(channel, True)
        
        # 4. Verify output is enabled
        output_enabled = dp2000.get_output_state(channel)
        assert output_enabled is True
        
        # 5. Read back settings
        voltage = dp2000.get_voltage(channel)
        current = dp2000.get_current(channel)
        assert voltage == 5.0
        assert current == 1.5
        
        # 6. Disable output
        dp2000.set_output_state(channel, False)
        
        # 7. Verify output is disabled
        final_state = dp2000.get_output_state(channel)
        assert final_state is False
        
        # Verify all commands were sent
        expected_writes = [
            ":SOUR1:VOLT 5.000000",
            ":SOUR1:CURR 1.500000", 
            ":OUTP1 ON",
            ":OUTP1 OFF"
        ]
        
        actual_writes = [call[0][0] for call in mock_session.write.call_args_list]
        for expected in expected_writes:
            assert expected in actual_writes
    
    @patch('pyvisa.ResourceManager')
    def test_protection_system_integration(self, mock_rm_class):
        """Test protection system integration."""
        # Setup mock
        mock_rm = Mock()
        mock_session = Mock()
        mock_rm_class.return_value = mock_rm
        mock_rm.open_resource.return_value = mock_session
        
        # Configure responses
        mock_session.query.side_effect = [
            "RIGOL TECHNOLOGIES,DP2031,DP2D251800001,00.01.14",  # IDN
            "6.500000",  # OVP level
            "1.800000",  # OCP level
            "1",         # OVP enabled
            "1",         # OCP enabled
            "0"          # Protection not triggered
        ]
        
        dp2000 = DP2000()
        dp2000.connect("USB0::0x1AB1::0x0E11::DP2D251800001::INSTR")
        
        channel = 1
        
        # Configure protection settings
        protection = ProtectionSettings(
            ovp_level=6.5,
            ovp_enabled=True,
            ocp_level=1.8,
            ocp_enabled=True
        )
        
        # Apply protection settings
        dp2000.configure_protection(channel, protection)
        
        # Verify protection settings
        ovp_level = dp2000.get_ovp_level(channel)
        ocp_level = dp2000.get_ocp_level(channel)
        ovp_enabled = dp2000.get_ovp_state(channel)
        ocp_enabled = dp2000.get_ocp_state(channel)
        
        assert ovp_level == 6.5
        assert ocp_level == 1.8
        assert ovp_enabled is True
        assert ocp_enabled is True
        
        # Check protection status
        protection_triggered = dp2000.check_protection_status(channel)
        assert protection_triggered is False
    
    @patch('pyvisa.ResourceManager')
    def test_error_recovery_integration(self, mock_rm_class):
        """Test error recovery in integrated system."""
        # Setup mock with connection failure and recovery
        mock_rm = Mock()
        mock_session = Mock()
        mock_rm_class.return_value = mock_rm
        mock_rm.open_resource.return_value = mock_session
        
        # Simulate connection lost during operation
        mock_session.query.side_effect = [
            "RIGOL TECHNOLOGIES,DP2031,DP2D251800001,00.01.14",  # Initial IDN
            Exception("VI_ERROR_CONN_LOST"),  # Connection lost
            "RIGOL TECHNOLOGIES,DP2031,DP2D251800001,00.01.14",  # Reconnect IDN
            "5.000000"  # Successful measurement after recovery
        ]
        
        dp2000 = DP2000()
        dp2000.connect("USB0::0x1AB1::0x0E11::DP2D251800001::INSTR")
        
        # Enable auto-reconnection
        dp2000.visa_session.auto_reconnect = True
        
        # First query should trigger reconnection
        voltage = dp2000.get_voltage(1)
        
        # Should succeed after reconnection
        assert voltage == 5.0
        
        # Verify statistics
        stats = dp2000.visa_session.get_statistics()
        assert stats['reconnections'] == 1
        assert stats['errors'] >= 1
    
    @patch('pyvisa.ResourceManager')
    def test_multi_channel_coordination(self, mock_rm_class):
        """Test coordinated control of multiple channels."""
        # Setup mock
        mock_rm = Mock()
        mock_session = Mock()
        mock_rm_class.return_value = mock_rm
        mock_rm.open_resource.return_value = mock_session
        
        # Configure responses for 3-channel operation
        mock_session.query.side_effect = [
            "RIGOL TECHNOLOGIES,DP2031,DP2D251800001,00.01.14",  # IDN
            "5.000000,1.000000,5.000000",   # CH1 measurement
            "3.300000,0.500000,1.650000",   # CH2 measurement  
            "12.000000,0.200000,2.400000",  # CH3 measurement
            "0", "0", "0",  # All outputs initially OFF
            "1", "1", "1"   # All outputs ON after enable
        ]
        
        dp2000 = DP2000()
        dp2000.connect("USB0::0x1AB1::0x0E11::DP2D251800001::INSTR")
        
        # Configure all channels
        channel_configs = [
            (1, 5.0, 1.0),    # 5V, 1A
            (2, 3.3, 0.5),    # 3.3V, 0.5A
            (3, 12.0, 0.2)    # 12V, 0.2A
        ]
        
        # Set all channel parameters
        for channel, voltage, current in channel_configs:
            dp2000.set_voltage(channel, voltage)
            dp2000.set_current(channel, current)
        
        # Measure all channels
        measurements = {}
        for channel, _, _ in channel_configs:
            measurements[channel] = dp2000.measure_all(channel)
        
        # Verify measurements match configurations
        for channel, voltage, current in channel_configs:
            meas = measurements[channel]
            assert abs(meas.voltage - voltage) < 0.1
            assert abs(meas.current - current) < 0.1
        
        # Enable all outputs sequentially
        for channel, _, _ in channel_configs:
            initial_state = dp2000.get_output_state(channel)
            assert initial_state is False
            
            dp2000.set_output_state(channel, True)
            
            final_state = dp2000.get_output_state(channel)
            assert final_state is True
    
    def test_data_model_integration(self):
        """Test integration of data models with measurements."""
        # Create sample measurements
        measurements = []
        base_time = time.time()
        
        for i in range(5):
            meas = ChannelMeasurement(
                timestamp=base_time + i,
                voltage=5.0 + i * 0.1,
                current=1.0 + i * 0.05,
                power=(5.0 + i * 0.1) * (1.0 + i * 0.05)
            )
            measurements.append(meas)
        
        # Verify measurement sequence
        assert len(measurements) == 5
        
        # Check that values change over time
        assert measurements[0].voltage != measurements[-1].voltage
        assert measurements[0].current != measurements[-1].current
        
        # Verify power calculation consistency
        for meas in measurements:
            expected_power = meas.voltage * meas.current
            assert abs(meas.power - expected_power) < 1e-6
        
        # Test protection settings validation
        valid_protection = ProtectionSettings(
            ovp_level=6.0,
            ovp_enabled=True,
            ocp_level=1.5,
            ocp_enabled=True
        )
        
        assert valid_protection.ovp_level == 6.0
        assert valid_protection.ocp_level == 1.5
        assert valid_protection.ovp_enabled is True
        assert valid_protection.ocp_enabled is True


@pytest.mark.integration
@pytest.mark.slow
class TestPerformanceIntegration:
    """Performance and timing integration tests."""
    
    @patch('pyvisa.ResourceManager')
    def test_measurement_timing(self, mock_rm_class):
        """Test measurement timing performance."""
        # Setup fast mock responses
        mock_rm = Mock()
        mock_session = Mock()
        mock_rm_class.return_value = mock_rm
        mock_rm.open_resource.return_value = mock_session
        
        # Fast responses for timing test
        mock_session.query.side_effect = [
            "RIGOL TECHNOLOGIES,DP2031,DP2D251800001,00.01.14"  # IDN
        ] + ["5.000000,1.000000,5.000000"] * 100  # 100 measurements
        
        dp2000 = DP2000()
        dp2000.connect("USB0::0x1AB1::0x0E11::DP2D251800001::INSTR")
        
        # Time multiple measurements
        start_time = time.time()
        measurements = []
        
        for _ in range(100):
            meas = dp2000.measure_all(1)
            measurements.append(meas)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Should complete 100 measurements in reasonable time
        assert len(measurements) == 100
        assert total_time < 5.0  # Less than 5 seconds
        
        # Calculate measurement rate
        rate = len(measurements) / total_time
        assert rate > 20  # At least 20 measurements per second
    
    @patch('pyvisa.ResourceManager')
    def test_connection_reliability(self, mock_rm_class):
        """Test connection reliability over multiple operations."""
        # Setup mock with occasional failures
        mock_rm = Mock()
        mock_session = Mock()
        mock_rm_class.return_value = mock_rm
        mock_rm.open_resource.return_value = mock_session
        
        # Mix of successful and failed operations
        responses = ["RIGOL TECHNOLOGIES,DP2031,DP2D251800001,00.01.14"]
        for i in range(50):
            if i % 10 == 9:  # Every 10th operation fails
                responses.append(Exception("Temporary failure"))
                responses.append("5.000000")  # Recovery response
            else:
                responses.append("5.000000")
        
        mock_session.query.side_effect = responses
        
        dp2000 = DP2000()
        dp2000.connect("USB0::0x1AB1::0x0E11::DP2D251800001::INSTR")
        dp2000.visa_session.auto_reconnect = True
        
        # Perform many operations with some failures
        successful_operations = 0
        for _ in range(50):
            try:
                voltage = dp2000.get_voltage(1)
                if voltage == 5.0:
                    successful_operations += 1
            except Exception:
                pass  # Expected occasional failures
        
        # Should have high success rate despite failures
        success_rate = successful_operations / 50
        assert success_rate > 0.8  # At least 80% success rate


if __name__ == "__main__":
    # Run integration tests
    pytest.main([__file__, "-v", "--tb=short", "-m", "integration"])
