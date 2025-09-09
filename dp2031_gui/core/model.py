"""
Data Models for DP2031 Power Controller

Defines data structures for power supply state, channel configuration,
protection settings, and operational modes.
"""

import time
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from enum import Enum, auto


class OutputMode(Enum):
    """Power supply output modes."""
    CV = "CV"  # Constant Voltage
    CC = "CC"  # Constant Current
    UR = "UR"  # Unregulated


class ProtectionState(Enum):
    """Protection states."""
    NORMAL = auto()
    OVP_TRIP = auto()  # Over Voltage Protection
    OCP_TRIP = auto()  # Over Current Protection  
    OTP_TRIP = auto()  # Over Temperature Protection


class SamplingMode(Enum):
    """Current sampling modes."""
    AUTO = "AUTO"
    HIGH = "HIGH"
    LOW = "LOW"


class PairMode(Enum):
    """Channel pairing modes."""
    NONE = "NONE"
    SERIES = "SER"
    PARALLEL = "PAR"


@dataclass
class ChannelMeasurement:
    """Single measurement from a power supply channel."""
    timestamp: float
    voltage: float
    current: float
    power: float
    
    @classmethod
    def now(cls, voltage: float, current: float, power: Optional[float] = None):
        """Create measurement with current timestamp."""
        if power is None:
            power = voltage * current
        return cls(
            timestamp=time.time(),
            voltage=voltage,
            current=current,
            power=power
        )


@dataclass
class ProtectionSettings:
    """Protection settings for a channel."""
    ovp_level: float = 0.0
    ovp_enabled: bool = False
    ocp_level: float = 0.0
    ocp_enabled: bool = False
    
    def __post_init__(self):
        """Validate protection settings."""
        if self.ovp_level < 0:
            raise ValueError("OVP level cannot be negative")
        if self.ocp_level < 0:
            raise ValueError("OCP level cannot be negative")


@dataclass  
class ChannelSetpoints:
    """Setpoint values for a channel."""
    voltage: float = 0.0
    current: float = 0.0
    
    def __post_init__(self):
        """Validate setpoints."""
        if self.voltage < 0:
            raise ValueError("Voltage setpoint cannot be negative")
        if self.current < 0:
            raise ValueError("Current setpoint cannot be negative")


@dataclass
class ChannelState:
    """Complete state of a power supply channel."""
    channel: int
    setpoints: ChannelSetpoints = field(default_factory=ChannelSetpoints)
    measurement: Optional[ChannelMeasurement] = None
    output_enabled: bool = False
    output_mode: OutputMode = OutputMode.CV
    protection: ProtectionSettings = field(default_factory=ProtectionSettings)
    protection_state: ProtectionState = ProtectionState.NORMAL
    remote_sense: bool = False
    
    # Measurement history for trending
    measurement_history: List[ChannelMeasurement] = field(default_factory=list)
    max_history: int = 1000  # Maximum measurements to keep
    
    def add_measurement(self, measurement: ChannelMeasurement) -> None:
        """Add measurement to history with automatic cleanup."""
        self.measurement = measurement
        self.measurement_history.append(measurement)
        
        # Trim history if too long
        if len(self.measurement_history) > self.max_history:
            self.measurement_history = self.measurement_history[-self.max_history:]
    
    def get_recent_measurements(self, count: int = 100) -> List[ChannelMeasurement]:
        """Get most recent measurements."""
        return self.measurement_history[-count:]
    
    def clear_history(self) -> None:
        """Clear measurement history."""
        self.measurement_history.clear()


@dataclass
class SystemStatus:
    """Overall system status."""
    timestamp: float = field(default_factory=time.time)
    connected: bool = False
    instrument_id: str = ""
    
    # Status register values
    status_byte: int = 0
    operation_condition: int = 0
    questionable_condition: int = 0
    
    # System settings
    sampling_mode: SamplingMode = SamplingMode.AUTO
    pair_mode: PairMode = PairMode.NONE
    tracking_enabled: bool = False
    remote_control: bool = False
    
    # Error information
    error_queue: List[str] = field(default_factory=list)
    last_error: Optional[str] = None
    
    def add_error(self, error: str) -> None:
        """Add error to queue."""
        self.error_queue.append(error)
        self.last_error = error
        
        # Limit error queue size
        if len(self.error_queue) > 100:
            self.error_queue = self.error_queue[-100:]
    
    def clear_errors(self) -> None:
        """Clear error queue."""
        self.error_queue.clear()
        self.last_error = None


@dataclass
class PowerSupplyModel:
    """Complete power supply model with all channels and system state."""
    
    # Channel states (DP2031 has 3 channels)
    channels: Dict[int, ChannelState] = field(default_factory=dict)
    
    # System status
    system: SystemStatus = field(default_factory=SystemStatus)
    
    # Configuration
    num_channels: int = 3
    
    def __post_init__(self):
        """Initialize channel states."""
        if not self.channels:
            for ch in range(1, self.num_channels + 1):
                self.channels[ch] = ChannelState(channel=ch)
    
    def get_channel(self, channel: int) -> ChannelState:
        """Get channel state, creating if necessary."""
        if channel not in self.channels:
            if 1 <= channel <= self.num_channels:
                self.channels[channel] = ChannelState(channel=channel)
            else:
                raise ValueError(f"Invalid channel number: {channel}")
        return self.channels[channel]
    
    def update_measurement(self, channel: int, voltage: float, current: float, power: Optional[float] = None) -> None:
        """Update measurement for a channel."""
        ch_state = self.get_channel(channel)
        measurement = ChannelMeasurement.now(voltage, current, power)
        ch_state.add_measurement(measurement)
    
    def set_output_state(self, channel: int, enabled: bool) -> None:
        """Set output state for a channel."""
        ch_state = self.get_channel(channel)
        ch_state.output_enabled = enabled
    
    def set_setpoints(self, channel: int, voltage: float, current: float) -> None:
        """Set voltage and current setpoints for a channel."""
        ch_state = self.get_channel(channel)
        ch_state.setpoints = ChannelSetpoints(voltage=voltage, current=current)
    
    def set_protection(self, channel: int, ovp_level: float = None, ovp_enabled: bool = None,
                      ocp_level: float = None, ocp_enabled: bool = None) -> None:
        """Set protection parameters for a channel."""
        ch_state = self.get_channel(channel)
        
        if ovp_level is not None:
            ch_state.protection.ovp_level = ovp_level
        if ovp_enabled is not None:
            ch_state.protection.ovp_enabled = ovp_enabled
        if ocp_level is not None:
            ch_state.protection.ocp_level = ocp_level
        if ocp_enabled is not None:
            ch_state.protection.ocp_enabled = ocp_enabled
    
    def get_all_measurements(self) -> Dict[int, Optional[ChannelMeasurement]]:
        """Get latest measurements from all channels."""
        return {ch: state.measurement for ch, state in self.channels.items()}
    
    def get_channel_data_for_trending(self, channel: int, max_points: int = 1000) -> Dict[str, List[float]]:
        """Get channel data formatted for trending plots."""
        ch_state = self.get_channel(channel)
        measurements = ch_state.get_recent_measurements(max_points)
        
        return {
            'timestamps': [m.timestamp for m in measurements],
            'voltages': [m.voltage for m in measurements],
            'currents': [m.current for m in measurements],
            'powers': [m.power for m in measurements]
        }
    
    def clear_all_history(self) -> None:
        """Clear measurement history for all channels."""
        for ch_state in self.channels.values():
            ch_state.clear_history()
    
    def get_system_summary(self) -> Dict[str, Any]:
        """Get summary of system state."""
        return {
            'connected': self.system.connected,
            'instrument_id': self.system.instrument_id,
            'channels_enabled': [ch for ch, state in self.channels.items() if state.output_enabled],
            'total_power': sum(
                state.measurement.power if state.measurement else 0.0 
                for state in self.channels.values()
            ),
            'error_count': len(self.system.error_queue),
            'last_error': self.system.last_error,
            'sampling_mode': self.system.sampling_mode.value,
            'pair_mode': self.system.pair_mode.value,
            'tracking_enabled': self.system.tracking_enabled
        }


@dataclass
class PresetConfiguration:
    """Saved configuration preset."""
    name: str
    description: str = ""
    timestamp: float = field(default_factory=time.time)
    
    # Channel configurations
    channel_setpoints: Dict[int, ChannelSetpoints] = field(default_factory=dict)
    channel_protection: Dict[int, ProtectionSettings] = field(default_factory=dict)
    channel_outputs: Dict[int, bool] = field(default_factory=dict)
    
    # System settings
    sampling_mode: SamplingMode = SamplingMode.AUTO
    pair_mode: PairMode = PairMode.NONE
    tracking_enabled: bool = False
    
    @classmethod
    def from_model(cls, model: PowerSupplyModel, name: str, description: str = "") -> 'PresetConfiguration':
        """Create preset from current model state."""
        return cls(
            name=name,
            description=description,
            channel_setpoints={ch: state.setpoints for ch, state in model.channels.items()},
            channel_protection={ch: state.protection for ch, state in model.channels.items()},
            channel_outputs={ch: state.output_enabled for ch, state in model.channels.items()},
            sampling_mode=model.system.sampling_mode,
            pair_mode=model.system.pair_mode,
            tracking_enabled=model.system.tracking_enabled
        )
    
    def apply_to_model(self, model: PowerSupplyModel) -> None:
        """Apply preset configuration to model."""
        # Update channel configurations
        for ch, setpoints in self.channel_setpoints.items():
            if ch in model.channels:
                model.channels[ch].setpoints = setpoints
        
        for ch, protection in self.channel_protection.items():
            if ch in model.channels:
                model.channels[ch].protection = protection
        
        for ch, output_enabled in self.channel_outputs.items():
            if ch in model.channels:
                model.channels[ch].output_enabled = output_enabled
        
        # Update system settings
        model.system.sampling_mode = self.sampling_mode
        model.system.pair_mode = self.pair_mode
        model.system.tracking_enabled = self.tracking_enabled
