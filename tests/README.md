# Testing Documentation for DP2031 Industrial Power Controller

## Overview

This document describes the comprehensive testing strategy for the DP2031 Industrial Power Controller project. The testing framework ensures reliability, maintainability, and quality of the industrial control application.

## Test Structure

```
tests/
├── conftest.py              # Test configuration and fixtures
├── test_scpi_parse.py       # SCPI parsing and validation tests
├── test_visa.py             # VISA communication tests
├── test_integration.py      # Integration and system tests
└── data/                    # Test data files
```

## Test Categories

### 1. Unit Tests

**Purpose**: Test individual components in isolation
**Location**: `test_scpi_parse.py`, `test_visa.py`

- **SCPI Command Parsing**: Validates SCPI response parsing, command formatting, and parameter validation
- **VISA Session Management**: Tests connection handling, error recovery, and statistics tracking
- **Data Model Validation**: Ensures data structures work correctly with proper validation

### 2. Integration Tests

**Purpose**: Test component interactions and complete workflows
**Location**: `test_integration.py`

- **Complete Measurement Cycles**: End-to-end testing from connection to data acquisition
- **Multi-Channel Coordination**: Tests coordinated control of multiple power supply channels
- **Protection System Integration**: Validates protection settings and alarm handling
- **Error Recovery Workflows**: Tests automatic reconnection and error handling

### 3. Performance Tests

**Purpose**: Validate timing requirements and performance characteristics
**Markers**: `@pytest.mark.slow`

- **Measurement Rate Testing**: Ensures 5-20Hz measurement capability
- **Connection Reliability**: Tests stability over extended operations
- **Memory Usage**: Validates memory efficiency for long-running operations

## Test Configuration

### pytest.ini

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --strict-config
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow-running tests
    hardware: Tests requiring actual hardware
```

### Fixtures

**Global Fixtures** (in `conftest.py`):
- `mock_visa_rm`: Mock VISA ResourceManager for testing
- `sample_dp2031_responses`: Realistic instrument responses
- `sample_measurements`: Test measurement data
- `test_data_dir`: Directory for test data files
- `temp_log_dir`: Temporary logging directory

## Running Tests

### Quick Test Run

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_scpi_parse.py

# Run with coverage
python -m pytest --cov=dp2031_gui --cov-report=html
```

### Windows Batch Script

```batch
# Run complete test suite with coverage
run_tests.bat
```

### Test Categories

```bash
# Unit tests only
python -m pytest -m "unit"

# Integration tests only  
python -m pytest -m "integration"

# Skip slow tests
python -m pytest -m "not slow"

# Skip hardware tests (default)
python -m pytest -m "not hardware"
```

## Test Data and Mocking

### Mock Strategy

- **PyVISA Mocking**: Complete mocking of VISA communication layer
- **Realistic Responses**: Use actual DP2031 response formats
- **Error Simulation**: Inject realistic communication errors
- **State Tracking**: Mock maintains instrument state consistency

### Sample Data

```python
# Sample SCPI responses
SAMPLE_RESPONSES = {
    'idn': "RIGOL TECHNOLOGIES,DP2031,DP2D251800001,00.01.14",
    'voltage': "5.000000",
    'current': "1.234567", 
    'all_measurement': "5.000000,1.234567,6.172839"
}
```

## Coverage Requirements

### Target Coverage

- **Overall Coverage**: > 90%
- **Core Modules**: > 95%
- **Critical Functions**: 100%

### Coverage Reports

```bash
# Generate HTML coverage report
python -m pytest --cov=dp2031_gui --cov-report=html:htmlcov

# View report
start htmlcov/index.html  # Windows
open htmlcov/index.html   # macOS
```

## Test Patterns

### 1. Arrange-Act-Assert Pattern

```python
def test_voltage_setting():
    # Arrange
    dp2000 = DP2000()
    channel = 1
    voltage = 5.0
    
    # Act
    dp2000.set_voltage(channel, voltage)
    
    # Assert
    mock_session.write.assert_called_with(":SOUR1:VOLT 5.000000")
```

### 2. Parameterized Tests

```python
@pytest.mark.parametrize("channel,voltage,expected", [
    (1, 5.0, ":SOUR1:VOLT 5.000000"),
    (2, 3.3, ":SOUR2:VOLT 3.300000"),
    (3, 12.0, ":SOUR3:VOLT 12.000000"),
])
def test_voltage_commands(channel, voltage, expected):
    # Test implementation
```

### 3. Context Managers

```python
def test_visa_context_manager():
    with VISASession() as session:
        session.connect("USB0::0x1AB1::0x0E11::DP2D251800001::INSTR")
        assert session.is_connected
    # Automatically disconnected
```

## Error Testing

### 1. Exception Handling

```python
def test_connection_failure():
    with pytest.raises(VISAError):
        session = VISASession()
        session.connect("INVALID::RESOURCE")
```

### 2. Recovery Testing

```python
def test_auto_reconnection():
    # Simulate connection loss
    mock_session.query.side_effect = [
        "RIGOL TECHNOLOGIES,DP2031,DP2D251800001,00.01.14",
        Exception("VI_ERROR_CONN_LOST"),
        "RIGOL TECHNOLOGIES,DP2031,DP2D251800001,00.01.14",
        "5.000000"
    ]
    
    # Should recover automatically
    voltage = dp2000.get_voltage(1)
    assert voltage == 5.0
```

## Continuous Integration

### Test Automation

```yaml
# GitHub Actions example
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run tests
        run: python -m pytest --cov=dp2031_gui --cov-report=xml
```

## Performance Benchmarking

### Measurement Rate Testing

```python
def test_measurement_rate():
    start_time = time.time()
    measurements = []
    
    for _ in range(100):
        meas = dp2000.measure_all(1)
        measurements.append(meas)
    
    elapsed = time.time() - start_time
    rate = len(measurements) / elapsed
    
    assert rate >= 20  # Minimum 20 measurements/second
```

### Memory Testing

```python
def test_memory_usage():
    import psutil
    import gc
    
    process = psutil.Process()
    initial_memory = process.memory_info().rss
    
    # Perform many operations
    for _ in range(1000):
        dp2000.measure_all(1)
    
    gc.collect()
    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory
    
    # Should not leak significant memory
    assert memory_increase < 10 * 1024 * 1024  # Less than 10MB
```

## Best Practices

### 1. Test Isolation

- Each test should be independent
- Use fresh mocks for each test
- Clean up resources in teardown

### 2. Realistic Testing

- Use actual SCPI command formats
- Test with realistic data ranges
- Include edge cases and error conditions

### 3. Documentation

- Clear test names describing what is tested
- Comments explaining complex test scenarios
- Docstrings for test classes and methods

### 4. Maintainability

- Keep tests simple and focused
- Avoid duplicating production code logic
- Use fixtures for common setup

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure project root is in Python path
2. **Mock Configuration**: Verify mock return values match expected formats
3. **Timing Issues**: Use appropriate timeouts for slow operations
4. **Resource Cleanup**: Ensure proper cleanup in test teardown

### Debug Tips

```python
# Enable verbose logging in tests
import logging
logging.basicConfig(level=logging.DEBUG)

# Use pytest debugging
pytest --pdb  # Drop to debugger on failure
pytest --pdbcls=IPython.terminal.debugger:Pdb  # Use IPython debugger
```

## Future Enhancements

1. **Hardware-in-the-Loop Testing**: Tests with actual DP2031 instruments
2. **Load Testing**: Extended duration and stress testing
3. **GUI Testing**: Automated UI testing with pytest-qt
4. **Compliance Testing**: IEC 61010 safety standard validation
