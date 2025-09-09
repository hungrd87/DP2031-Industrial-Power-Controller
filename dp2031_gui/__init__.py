"""
DP2031 Industrial Power Controller

A professional PyQt6-based application for controlling RIGOL DP2000/DP2031 power supplies
with industrial-style GUI interface and real-time monitoring capabilities.

Author: Industrial Control Systems
Version: 1.0.0
Python: 3.11+
"""

__version__ = "1.0.0"
__author__ = "Industrial Control Systems"
__email__ = "support@instrumentcontrol.local"

# Package information
__title__ = "DP2031 Industrial Power Controller"
__description__ = "Professional RIGOL DP2000/DP2031 Power Supply Control Application"
__url__ = "https://github.com/industrial-control/dp2031-controller"

# Version info tuple for programmatic access
__version_info__ = tuple(map(int, __version__.split('.')))

# Export main components
from .core.dp2000_scpi import DP2000
from .core.visa_session import VISASession
from .core.model import PowerSupplyModel, ChannelState

__all__ = [
    'DP2000',
    'VISASession', 
    'PowerSupplyModel',
    'ChannelState',
    '__version__',
    '__version_info__'
]
