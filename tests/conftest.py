"""
Test configuration and pytest setup for DP2031 project.

Configures test environment, fixtures, and common utilities
for testing the industrial power supply controller.
"""

import pytest
import sys
import logging
from pathlib import Path
from unittest.mock import Mock, MagicMock

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configure logging for tests
logging.basicConfig(
    level=logging.WARNING,  # Reduce noise during testing
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Disable VISA logging during tests
logging.getLogger('pyvisa').setLevel(logging.ERROR)
logging.getLogger('dp2031_gui').setLevel(logging.WARNING)


@pytest.fixture
def mock_visa_rm():
    """Mock VISA ResourceManager for testing."""
    with pytest.importorskip("pyvisa"):
        mock_rm = MagicMock()
        mock_session = MagicMock()
        
        # Configure mock session
        mock_session.query.return_value = "RIGOL TECHNOLOGIES,DP2031,DP2D251800001,00.01.14"
        mock_session.write.return_value = None
        mock_session.timeout = 5000
        
        # Configure mock resource manager
        mock_rm.open_resource.return_value = mock_session
        mock_rm.list_resources.return_value = [
            "USB0::0x1AB1::0x0E11::DP2D251800001::INSTR",
            "TCPIP0::192.168.1.100::INSTR"
        ]
        
        return mock_rm, mock_session


@pytest.fixture
def sample_dp2031_responses():
    """Sample responses from DP2031 instrument."""
    return {
        'idn': "RIGOL TECHNOLOGIES,DP2031,DP2D251800001,00.01.14",
        'voltage_ch1': "5.000000",
        'current_ch1': "1.234567",
        'power_ch1': "6.172839",
        'all_ch1': "5.000000,1.234567,6.172839",
        'output_state_on': "1",
        'output_state_off': "0",
        'ovp_level': "6.500000",
        'ocp_level': "1.500000",
        'protection_triggered': "1",
        'protection_ok': "0",
        'status_byte': "64",
        'operation_condition': "256",
        'error_none': "0,\"No error\"",
        'error_syntax': "-102,\"Syntax error\"",
        'error_undefined': "-113,\"Undefined header\""
    }


@pytest.fixture
def sample_measurements():
    """Sample measurement data for testing."""
    import time
    from dp2031_gui.core.model import ChannelMeasurement
    
    base_time = time.time()
    return [
        ChannelMeasurement(
            timestamp=base_time,
            voltage=5.0,
            current=1.0,
            power=5.0
        ),
        ChannelMeasurement(
            timestamp=base_time + 1,
            voltage=5.1,
            current=1.1,
            power=5.61
        ),
        ChannelMeasurement(
            timestamp=base_time + 2,
            voltage=4.9,
            current=0.9,
            power=4.41
        )
    ]


@pytest.fixture
def test_data_dir():
    """Directory for test data files."""
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    return data_dir


@pytest.fixture
def temp_log_dir(tmp_path):
    """Temporary directory for log files during testing."""
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    return log_dir


class TestUtilities:
    """Common utilities for testing."""
    
    @staticmethod
    def create_mock_dp2000():
        """Create a mock DP2000 instance for testing."""
        from dp2031_gui.core.dp2000_scpi import DP2000
        
        mock_dp2000 = Mock(spec=DP2000)
        mock_dp2000.is_connected = True
        mock_dp2000.model = "DP2031"
        mock_dp2000.serial_number = "DP2D251800001"
        mock_dp2000.firmware_version = "00.01.14"
        
        # Configure method return values
        mock_dp2000.connect.return_value = True
        mock_dp2000.disconnect.return_value = True
        mock_dp2000.get_identification.return_value = {
            'manufacturer': 'RIGOL TECHNOLOGIES',
            'model': 'DP2031',
            'serial_number': 'DP2D251800001',
            'firmware_version': '00.01.14'
        }
        
        return mock_dp2000
    
    @staticmethod
    def assert_measurement_equal(meas1, meas2, tolerance=1e-6):
        """Assert two measurements are equal within tolerance."""
        assert abs(meas1.voltage - meas2.voltage) < tolerance
        assert abs(meas1.current - meas2.current) < tolerance
        assert abs(meas1.power - meas2.power) < tolerance
    
    @staticmethod
    def create_test_csv_data():
        """Create sample CSV data for testing."""
        import io
        csv_data = io.StringIO()
        csv_data.write("timestamp,channel,voltage,current,power\n")
        csv_data.write("1234567890.123,1,5.000,1.000,5.000\n")
        csv_data.write("1234567891.123,1,5.100,1.100,5.610\n")
        csv_data.write("1234567892.123,1,4.900,0.900,4.410\n")
        csv_data.seek(0)
        return csv_data.getvalue()


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "hardware: mark test as requiring hardware"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        # Add markers based on test file names
        if "test_integration" in item.fspath.basename:
            item.add_marker(pytest.mark.integration)
        
        if "test_hardware" in item.fspath.basename:
            item.add_marker(pytest.mark.hardware)
        
        # Add markers based on test names
        if "slow" in item.name.lower():
            item.add_marker(pytest.mark.slow)


# Skip hardware tests by default
def pytest_runtest_setup(item):
    """Setup for each test item."""
    if "hardware" in item.keywords:
        pytest.skip("Hardware tests skipped by default")


# Test data constants
TEST_INSTRUMENT_RESOURCES = [
    "USB0::0x1AB1::0x0E11::DP2D251800001::INSTR",
    "TCPIP0::192.168.1.100::5555::SOCKET",
    "ASRL3::INSTR",
    "GPIB0::7::INSTR"
]

TEST_SCPI_COMMANDS = {
    'identification': '*IDN?',
    'reset': '*RST',
    'clear_status': '*CLS',
    'operation_complete': '*OPC?',
    'self_test': '*TST?',
    'error_query': 'SYST:ERR?',
    'voltage_set': ':SOUR{ch}:VOLT {value}',
    'current_set': ':SOUR{ch}:CURR {value}',
    'output_on': ':OUTP{ch} ON',
    'output_off': ':OUTP{ch} OFF',
    'voltage_measure': ':MEAS:SCAL:VOLT:DC? CH{ch}',
    'current_measure': ':MEAS:SCAL:CURR:DC? CH{ch}',
    'power_measure': ':MEAS:SCAL:POW:DC? CH{ch}',
    'all_measure': ':MEAS:SCAL:ALL:DC? CH{ch}'
}

TEST_CHANNEL_LIMITS = {
    'voltage_min': 0.0,
    'voltage_max': 64.0,
    'current_min': 0.0,
    'current_max': 10.0,
    'power_max': 640.0,
    'channels': [1, 2, 3]
}
