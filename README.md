# DP2031 Industrial Power Controller

A professional Python application for controlling RIGOL DP2000/DP2031 power supplies with modern PyQt6 industrial GUI interface.

![Version](https://img.shields.io/badge/version-v1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.13.7-green.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.9.0-orange.svg)
![Status](https://img.shields.io/badge/status-production--ready-brightgreen.svg)

## 🎯 Project Overview

This application provides comprehensive control of RIGOL DP2000/DP2031 power supplies featuring:

- **Modern PyQt6 GUI**: Industrial design with professional appearance
- **Enhanced Connect Action**: Direct connection to last resource (1-click reconnection)
- **Theme System**: Light/Dark themes with complete consistency
- **3-Channel Control**: Precision voltage/current/power control
- **Real-time Monitoring**: Live data visualization and trending
- **Professional Layout**: Status dock with always-visible monitoring controls
- **EMERGENCY STOP**: Right-positioned with proper red styling
- **Data Logging**: Comprehensive CSV logging with timestamps

## 🚀 Latest Features (v1.0.0)

### 🔗 Enhanced Connect Action
- **Direct Connection**: Automatically connects to last successful resource
- **Smart Fallback**: Shows Connection Dialog for first-time use
- **1-Click Reconnection**: Reduced from 3+ clicks to single click
- **Settings Persistence**: Remembers last resource across app restarts

### 🎨 Complete Theme Integration
- **Fixed Theme Issues**: TabWidget, Menu, Toolbar now fully themed
- **Light/Dark Themes**: Professional color schemes
- **Industrial Styling**: Specialized widgets for power supply control
- **Consistent Appearance**: All UI elements follow theme

### 🏗️ Professional UI Layout
- **Status Dock Reorganization**: Monitoring controls always visible
- **Tab Prioritization**: Channel Status shown first
- **EMERGENCY STOP**: Professional right positioning with red text
- **Toolbar Enhancement**: Connect action and emergency controls

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

- **Python**: 3.11+ (Tested on 3.13.7)
- **Operating System**: Windows 10+ (Primary), Linux/macOS compatible
- **Hardware**: RIGOL DP2000/DP2031 Power Supply
- **Connection**: USB, LAN (VXI-11), RS-232, or GPIB interface
- **Dependencies**: See requirements.txt for complete list

## 🛠️ Technology Stack

- **GUI Framework**: PyQt6 6.9.0 for modern industrial interface
- **Communication**: PyVISA 1.15.0 with NI/Keysight backend
- **Real-time Plotting**: pyqtgraph 0.13.7 for high-performance displays
- **Scientific Computing**: NumPy 1.26.4 for data processing
- **Theme System**: Custom reusable theme manager
- **Testing**: pytest for comprehensive testing
- **Version Control**: Git with professional workflow
- **Logging**: Industrial-grade logging system

## 🎯 Quick Start

### Recommended Method (NEW)
```bash
# 1. Clone repository
git clone <repository-url>
cd DP2031

# 2. Setup virtual environment and dependencies  
setup_venv.bat

# 3. Run application using main.py
python main.py

# Or use batch script
run_main.bat
```

### Module Execution
```bash
# Direct module execution
python -m dp2031_gui

# Or use existing batch script
run_dp2031.bat
```

### Development Mode
```bash
# For development and troubleshooting
python debug.py

# Or use batch script for debugging
run_debug.bat
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
