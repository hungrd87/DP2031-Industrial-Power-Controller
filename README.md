# DP2031 Industrial Power Controller

A professional Python application for controlling RIGOL DP2000/DP2031 power supplies with industrial-style GUI interface.

## 🎯 Project Overview

This application provides comprehensive control of RIGOL DP2000/DP2031 power supplies featuring:

- **3-Channel Control**: Set/read V-I-P for all channels with precision
- **Industrial GUI**: Big digits, status lamps, alarms, E-Stop functionality  
- **Real-time Monitoring**: Live trending of voltage, current, and power
- **Protection Features**: OVP/OCP controls with alarm management
- **Advanced Modes**: Series/parallel/tracking, remote sense, low-current sampling
- **Data Logging**: CSV logging with configurable intervals
- **Auto-recovery**: Automatic connection recovery and error handling

## 🚀 Features

### Core Functionality
- **VISA Communication**: USB/LAN VXI-11 (optional RS-232/GPIB)
- **Multi-channel Control**: Independent control of 3 power channels
- **Real-time Acquisition**: 5-20 Hz polling with optimized performance
- **Protection Systems**: Comprehensive OVP/OCP/OTP monitoring
- **Industrial Interface**: Professional control panel design

### Advanced Features
- **Operational Modes**: Series/parallel coupling, tracking mode
- **Remote Sensing**: 4-wire measurement capability
- **Low-current Sampling**: Microamp measurement precision
- **Preset Management**: Save/recall configurations
- **Event Logging**: Comprehensive system and error logging
- **Alarm Management**: Real-time status monitoring and alerts

## 📋 System Requirements

- **Python**: 3.11+ (Recommended: 3.13.7)
- **Operating System**: Windows 10+ (Primary), Linux/macOS compatible
- **Hardware**: RIGOL DP2000/DP2031 Power Supply
- **Connection**: USB, LAN (VXI-11), RS-232, or GPIB interface

## 🛠️ Technology Stack

- **GUI Framework**: PyQt6 for modern industrial interface
- **Communication**: PyVISA with NI/Keysight backend
- **Real-time Plotting**: pyqtgraph for high-performance displays
- **Scientific Computing**: NumPy for data processing
- **Configuration**: python-dotenv for environment management
- **Testing**: pytest for comprehensive testing
- **Logging**: Python logging for system monitoring

## 🎯 Quick Start

### Option 1: Simple Main Entry (NEW - Recommended)
```bash
# 1. Setup virtual environment and dependencies
setup_venv.bat

# 2. Run application using main.py
python main.py

# Or use batch script
run_main.bat
```

### Option 2: Debug Mode (NEW)
```bash
# For development and troubleshooting
python debug.py

# Or use batch script
run_debug_main.bat
```

### Option 3: Quick Run (NEW)
```bash
# Minimal logging for quick testing
python quick_run.py

# Silent mode (errors only)
python quick_run.py --silent
```

### Option 4: Traditional Method
```bash
# Direct module execution
python -m dp2031_gui.app

# Or existing batch scripts
run_app.bat
run_debug.bat
```

### Option 5: Manual Setup
```bash
# 1. Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run application
python main.py
```

## 📂 Project Structure

```
DP2031/
├── .venv/                      # Virtual environment
├── main.py                     # NEW: Main entry point with banner
├── debug.py                    # NEW: Debug entry point with diagnostics
├── quick_run.py               # NEW: Quick start with minimal logging
├── run_main.bat               # NEW: Batch launcher for main.py
├── run_debug_main.bat         # NEW: Batch launcher for debug.py
├── dp2031_gui/                 # Main application package
│   ├── app.py                  # Application entry point
│   ├── core/                   # Core functionality
│   │   ├── visa_session.py     # VISA communication layer
│   │   ├── dp2000_scpi.py      # DP2000/DP2031 SCPI driver
│   │   ├── acquisition.py      # Real-time data acquisition
│   │   ├── model.py            # Data models and state
│   │   ├── storage.py          # Data logging (CSV/NPY)
│   │   ├── alarms.py           # Alarm and status management
│   │   └── logging_cfg.py      # Logging configuration
│   ├── ui/                     # User interface
│   │   ├── main_window.py      # Main application window
│   │   ├── widgets.py          # Custom industrial widgets
│   │   └── styles.qss          # Industrial styling
│   └── tests/                  # Test suite
│       ├── test_scpi_parse.py  # SCPI parsing tests
│       └── test_trend_perf.py  # Performance tests
├── requirements.txt            # Dependencies
├── setup_venv.bat             # Setup script
├── run_dp2031.bat             # Legacy run script
├── run_app.bat                # Application launcher
└── README.md                  # This file
```

## 🔌 VISA Connection Examples

### USB Connection
```python
resource = "USB0::0x1AB1::0x0E11::DP2D251800XXX::INSTR"
```

### LAN Connection (VXI-11)
```python
resource = "TCPIP0::192.168.1.120::INSTR"
```

### RS-232 Connection
```python
resource = "ASRL1::INSTR"  # COM1
```

## 🎮 User Interface

### Industrial Control Panels
- **Setpoints Dock**: Large digit displays for V/I settings with rotary controls
- **Status Dock**: LED indicators for CV/CC/UR, OVP/OCP/OTP, REMOTE/LOCAL modes
- **Trend Dock**: Real-time graphs for voltage, current, and power trending
- **Alarms Dock**: Event log with status decoding and trip reset controls
- **Control Bar**: Resource selection, connection control, E-Stop, preset management

### Key Features
- **Big Digits**: Easy-to-read numerical displays
- **Status Lamps**: Color-coded LED indicators
- **E-Stop**: Emergency shutdown functionality
- **Real-time Trends**: Live data visualization
- **Industrial Styling**: Professional gray/red/yellow/green color scheme

## 🔧 API Reference

### Basic Operations
```python
from dp2031_gui.core.dp2000_scpi import DP2000

# Initialize and connect
power_supply = DP2000()
power_supply.connect("TCPIP0::192.168.1.120::INSTR")

# Set voltage and current for channel 1
power_supply.set_vi(ch=1, volt=5.0, curr=1.0)

# Enable output
power_supply.output(ch=1, on=True)

# Read measurements
voltage, current, power = power_supply.read_all(ch=1)

# Set protection limits
power_supply.set_ovp(ch=1, level=6.5, enable=True)
power_supply.set_ocp(ch=1, level=1.2, enable=True)
```

### Advanced Features
```python
# Configure sampling mode for microamp measurements
power_supply.set_sampling("LOW")

# Set channels in series/parallel mode
power_supply.set_pair("SER")  # or "PAR"

# Enable tracking mode
power_supply.set_tracking(on=True)

# Enable remote sensing (4-wire)
power_supply.remote_sense(on=True)
```

## 📊 Performance Specifications

- **Acquisition Rate**: 5-20 Hz configurable
- **Display Update**: ≥30 FPS with decimation
- **Data Retention**: 5-10 minutes ring buffer
- **Response Time**: <10ms SCPI commands
- **Connection Recovery**: Automatic with retry logic

## 🧪 Testing

Run the test suite to verify functionality:

```bash
# Run all tests
pytest tests/

# Test SCPI parsing
pytest tests/test_scpi_parse.py

# Test trending performance
pytest tests/test_trend_perf.py
```

## 📝 Logging and Data Storage

- **System Logs**: Application events and errors
- **Data Logging**: CSV format with timestamps
- **Rolling Storage**: Configurable retention periods
- **Export Options**: CSV snapshots and NPY arrays

## 🔍 Troubleshooting

### Connection Issues
1. Verify VISA runtime installation (NI-VISA or Keysight IO Libraries)
2. Check instrument resource string
3. Ensure network connectivity for LAN connections
4. Verify USB drivers for USB connections

### Performance Issues
1. Adjust acquisition rate (5-20 Hz)
2. Enable data decimation for long-term trending
3. Check system resources and background processes

## 📚 Documentation References

- **DP2000 Programming Guide (2024)**: Complete SCPI command reference
- **User Manual**: Hardware setup and connection guide
- **RIGOL Website**: Product specifications and updates

## 🎉 Getting Started

1. **Hardware Setup**: Connect DP2000/DP2031 via USB or LAN
2. **Software Setup**: Run `setup_venv.bat` for first-time installation
3. **Launch Application**: Use `run_dp2031.bat` or manual startup
4. **Connect**: Select resource and establish connection
5. **Control**: Use industrial interface for power supply control

**Ready to control your RIGOL DP2000/DP2031 with professional precision!** 🚀
