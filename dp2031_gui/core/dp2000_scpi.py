"""
RIGOL DP2000/DP2031 SCPI Driver

High-level driver for RIGOL DP2000/DP2031 power supplies implementing
comprehensive SCPI command set with error handling and status monitoring.
"""

import logging
import time
from typing import Optional, Tuple, List, Union

from .visa_session import VISASession, VISAError
from .model import (
    PowerSupplyModel, ChannelState, OutputMode, ProtectionState,
    SamplingMode, PairMode, ChannelMeasurement
)

logger = logging.getLogger(__name__)


class DP2000Error(Exception):
    """Exception for DP2000-specific errors."""
    pass


class DP2000:
    """
    High-level driver for RIGOL DP2000/DP2031 Power Supplies.
    
    Provides comprehensive control of voltage, current, protection settings,
    and advanced features like series/parallel operation and tracking.
    """
    
    def __init__(self):
        """Initialize DP2000 driver."""
        self.visa_session = VISASession()
        self.model = PowerSupplyModel()
        self._last_error_check = time.time()
        self._error_check_interval = 1.0  # Check errors every second
        
        # Device capabilities (will be updated after connection)
        self.max_voltage = 64.0  # V
        self.max_current = 10.0  # A
        self.max_power = 222.0   # W
        self.num_channels = 3
        
    def __enter__(self):
        """Context manager entry."""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
    
    def connect(self, resource: str, **kwargs) -> None:
        """
        Connect to DP2000/DP2031 power supply.
        
        Args:
            resource: VISA resource string (USB/LAN/RS232)
            **kwargs: Additional connection parameters
        """
        try:
            self.visa_session.connect(resource, **kwargs)
            
            # Get instrument identification
            idn = self.idn()
            self.model.system.instrument_id = idn
            self.model.system.connected = True
            
            # Initialize instrument state
            self._initialize_instrument()
            
            logger.info(f"Successfully connected to {idn}")
            
        except Exception as e:
            self.model.system.connected = False
            logger.error(f"Failed to connect: {e}")
            raise DP2000Error(f"Connection failed: {e}")
    
    def close(self) -> None:
        """Close connection to power supply."""
        try:
            if self.model.system.connected:
                # Safety: Turn off all outputs before disconnect
                self.output_all(False)
                self.to_local()  # Return to local control
                
            self.visa_session.close()
            self.model.system.connected = False
            logger.info("Connection closed")
            
        except Exception as e:
            logger.warning(f"Error during close: {e}")
    
    def _initialize_instrument(self) -> None:
        """Initialize instrument after connection."""
        try:
            # Clear any existing errors
            self.clear_errors()
            
            # Set to remote control mode
            self.to_remote()
            
            # Read initial system status
            self._update_system_status()
            
            # Read initial channel states
            for ch in range(1, self.num_channels + 1):
                self._update_channel_state(ch)
            
            logger.info("Instrument initialization complete")
            
        except Exception as e:
            logger.error(f"Instrument initialization failed: {e}")
            raise DP2000Error(f"Initialization failed: {e}")
    
    def idn(self) -> str:
        """
        Get instrument identification.
        
        Returns:
            Instrument identification string
        """
        try:
            return self.visa_session.query("*IDN?").strip()
        except Exception as e:
            raise DP2000Error(f"Failed to get identification: {e}")
    
    def opc(self) -> None:
        """Wait for operation complete."""
        try:
            self.visa_session.query("*OPC?")
        except Exception as e:
            raise DP2000Error(f"OPC query failed: {e}")
    
    # Channel Basic Operations
    
    def set_vi(self, ch: int, volt: float, curr: float) -> None:
        """
        Set voltage and current for a channel.
        
        Args:
            ch: Channel number (1-3)
            volt: Voltage setpoint in volts
            curr: Current setpoint in amperes
        """
        self._validate_channel(ch)
        self._validate_voltage(volt)
        self._validate_current(curr)
        
        try:
            self.visa_session.write(f":SOUR{ch}:VOLT {volt:.6f}")
            self.visa_session.write(f":SOUR{ch}:CURR {curr:.6f}")
            
            # Update model
            self.model.set_setpoints(ch, volt, curr)
            
            self._check_errors()
            logger.debug(f"CH{ch}: Set V={volt:.3f}V, I={curr:.3f}A")
            
        except Exception as e:
            raise DP2000Error(f"Failed to set V/I for CH{ch}: {e}")
    
    def output(self, ch: int, on: bool) -> None:
        """
        Enable/disable output for a channel.
        
        Args:
            ch: Channel number (1-3)
            on: True to enable, False to disable
        """
        self._validate_channel(ch)
        
        try:
            state = "ON" if on else "OFF"
            self.visa_session.write(f":OUTP{ch} {state}")
            
            # Update model
            self.model.set_output_state(ch, on)
            
            self._check_errors()
            logger.info(f"CH{ch}: Output {state}")
            
        except Exception as e:
            raise DP2000Error(f"Failed to set output for CH{ch}: {e}")
    
    def output_all(self, on: bool) -> None:
        """
        Enable/disable all outputs simultaneously.
        
        Args:
            on: True to enable all, False to disable all
        """
        try:
            state = "ON" if on else "OFF"
            self.visa_session.write(f":OUTP:STAT {state}")
            
            # Update model for all channels
            for ch in range(1, self.num_channels + 1):
                self.model.set_output_state(ch, on)
            
            self._check_errors()
            logger.info(f"All outputs: {state}")
            
        except Exception as e:
            raise DP2000Error(f"Failed to set all outputs: {e}")
    
    def read_v(self, ch: int) -> float:
        """
        Read voltage measurement from a channel.
        
        Args:
            ch: Channel number (1-3)
            
        Returns:
            Voltage in volts
        """
        self._validate_channel(ch)
        
        try:
            response = self.visa_session.query(f":MEAS:SCAL:VOLT:DC? CH{ch}")
            voltage = float(response.strip())
            logger.debug(f"CH{ch}: Read V={voltage:.6f}V")
            return voltage
            
        except Exception as e:
            raise DP2000Error(f"Failed to read voltage for CH{ch}: {e}")
    
    def read_i(self, ch: int) -> float:
        """
        Read current measurement from a channel.
        
        Args:
            ch: Channel number (1-3)
            
        Returns:
            Current in amperes
        """
        self._validate_channel(ch)
        
        try:
            response = self.visa_session.query(f":MEAS:SCAL:CURR:DC? CH{ch}")
            current = float(response.strip())
            logger.debug(f"CH{ch}: Read I={current:.6f}A")
            return current
            
        except Exception as e:
            raise DP2000Error(f"Failed to read current for CH{ch}: {e}")
    
    def read_all(self, ch: int) -> Tuple[float, float, float]:
        """
        Read voltage, current, and power from a channel.
        
        Args:
            ch: Channel number (1-3)
            
        Returns:
            Tuple of (voltage, current, power)
        """
        self._validate_channel(ch)
        
        try:
            response = self.visa_session.query(f":MEAS:SCAL:ALL:DC? CH{ch}")
            values = response.strip().split(',')
            
            if len(values) != 3:
                raise ValueError(f"Expected 3 values, got {len(values)}")
            
            voltage = float(values[0])
            current = float(values[1])
            power = float(values[2])
            
            # Update model with measurement
            self.model.update_measurement(ch, voltage, current, power)
            
            logger.debug(f"CH{ch}: V={voltage:.6f}V, I={current:.6f}A, P={power:.6f}W")
            return voltage, current, power
            
        except Exception as e:
            raise DP2000Error(f"Failed to read all measurements for CH{ch}: {e}")
    
    # Protection Settings
    
    def set_ovp(self, ch: int, level: float, enable: bool = True) -> None:
        """
        Set over-voltage protection.
        
        Args:
            ch: Channel number (1-3)
            level: OVP level in volts
            enable: True to enable protection
        """
        self._validate_channel(ch)
        self._validate_voltage(level)
        
        try:
            self.visa_session.write(f":SOUR{ch}:VOLT:PROT:LEV {level:.6f}")
            state = "ON" if enable else "OFF"
            self.visa_session.write(f":SOUR{ch}:VOLT:PROT:STAT {state}")
            
            # Update model
            self.model.set_protection(ch, ovp_level=level, ovp_enabled=enable)
            
            self._check_errors()
            logger.info(f"CH{ch}: OVP set to {level:.3f}V ({state})")
            
        except Exception as e:
            raise DP2000Error(f"Failed to set OVP for CH{ch}: {e}")
    
    def set_ocp(self, ch: int, level: float, enable: bool = True) -> None:
        """
        Set over-current protection.
        
        Args:
            ch: Channel number (1-3)
            level: OCP level in amperes
            enable: True to enable protection
        """
        self._validate_channel(ch)
        self._validate_current(level)
        
        try:
            self.visa_session.write(f":SOUR{ch}:CURR:PROT:LEV {level:.6f}")
            state = "ON" if enable else "OFF"
            self.visa_session.write(f":SOUR{ch}:CURR:PROT:STAT {state}")
            
            # Update model
            self.model.set_protection(ch, ocp_level=level, ocp_enabled=enable)
            
            self._check_errors()
            logger.info(f"CH{ch}: OCP set to {level:.3f}A ({state})")
            
        except Exception as e:
            raise DP2000Error(f"Failed to set OCP for CH{ch}: {e}")
    
    def clear_trips(self, ch: int) -> None:
        """
        Clear protection trips for a channel.
        
        Args:
            ch: Channel number (1-3)
        """
        self._validate_channel(ch)
        
        try:
            self.visa_session.write(f":OUTP{ch}:OVP:CLEar")
            self.visa_session.write(f":OUTP{ch}:OCP:CLEar")
            
            # Update model - reset protection state
            ch_state = self.model.get_channel(ch)
            ch_state.protection_state = ProtectionState.NORMAL
            
            self._check_errors()
            logger.info(f"CH{ch}: Protection trips cleared")
            
        except Exception as e:
            raise DP2000Error(f"Failed to clear trips for CH{ch}: {e}")
    
    # System Features
    
    def set_sampling(self, mode: str = "AUTO") -> None:
        """
        Set current sampling mode.
        
        Args:
            mode: Sampling mode ("AUTO", "HIGH", "LOW")
        """
        if mode not in ["AUTO", "HIGH", "LOW"]:
            raise ValueError(f"Invalid sampling mode: {mode}")
        
        try:
            self.visa_session.write(f":SYST:SAMPling {mode}")
            
            # Update model
            self.model.system.sampling_mode = SamplingMode(mode)
            
            self._check_errors()
            logger.info(f"Sampling mode set to {mode}")
            
        except Exception as e:
            raise DP2000Error(f"Failed to set sampling mode: {e}")
    
    def set_pair(self, mode: Optional[str]) -> None:
        """
        Set channel pairing mode.
        
        Args:
            mode: Pairing mode ("SER", "PAR", "NONE" or None)
        """
        if mode is not None and mode not in ["SER", "PAR", "NONE"]:
            raise ValueError(f"Invalid pair mode: {mode}")
        
        try:
            if mode is None or mode == "NONE":
                # Disable pairing (implementation depends on specific model)
                self.visa_session.write(":OUTP:PAIR OFF")
                pair_mode = PairMode.NONE
            else:
                self.visa_session.write(f":OUTP:PAIR {mode}")
                pair_mode = PairMode(mode)
            
            # Update model
            self.model.system.pair_mode = pair_mode
            
            self._check_errors()
            logger.info(f"Pair mode set to {mode}")
            
        except Exception as e:
            logger.warning(f"Pair mode setting may not be supported: {e}")
    
    def set_tracking(self, on: bool) -> None:
        """
        Enable/disable tracking mode.
        
        Args:
            on: True to enable tracking
        """
        try:
            state = "ON" if on else "OFF"
            self.visa_session.write(f":OUTP:TRACk:STATe {state}")
            
            # Update model
            self.model.system.tracking_enabled = on
            
            self._check_errors()
            logger.info(f"Tracking mode: {state}")
            
        except Exception as e:
            logger.warning(f"Tracking mode may not be supported: {e}")
    
    def remote_sense(self, on: bool) -> None:
        """
        Enable/disable remote sensing (4-wire measurement).
        
        Args:
            on: True to enable remote sensing
        """
        try:
            # Implementation depends on specific model capabilities
            state = "ON" if on else "OFF"
            for ch in range(1, self.num_channels + 1):
                self.visa_session.write(f":SOUR{ch}:SENS:REM {state}")
                ch_state = self.model.get_channel(ch)
                ch_state.remote_sense = on
            
            self._check_errors()
            logger.info(f"Remote sensing: {state}")
            
        except Exception as e:
            logger.warning(f"Remote sensing may not be supported: {e}")
    
    def to_remote(self) -> None:
        """Switch instrument to remote control mode."""
        try:
            self.visa_session.write(":SYST:REM")
            self.model.system.remote_control = True
            logger.debug("Switched to remote control")
        except Exception as e:
            raise DP2000Error(f"Failed to switch to remote: {e}")
    
    def to_local(self) -> None:
        """Return instrument to local control mode."""
        try:
            self.visa_session.write(":SYST:LOC")
            self.model.system.remote_control = False
            logger.debug("Returned to local control")
        except Exception as e:
            logger.warning(f"Failed to return to local: {e}")
    
    # Status and Error Handling
    
    def read_stb(self) -> int:
        """
        Read status byte register.
        
        Returns:
            Status byte value
        """
        try:
            response = self.visa_session.query("*STB?")
            stb = int(response.strip())
            self.model.system.status_byte = stb
            return stb
        except Exception as e:
            raise DP2000Error(f"Failed to read status byte: {e}")
    
    def read_oper_cond(self) -> int:
        """
        Read operation condition register.
        
        Returns:
            Operation condition value
        """
        try:
            response = self.visa_session.query(":STAT:OPER:COND?")
            oper = int(response.strip())
            self.model.system.operation_condition = oper
            return oper
        except Exception as e:
            raise DP2000Error(f"Failed to read operation condition: {e}")
    
    def query_errors(self) -> List[str]:
        """
        Query and return all errors from error queue.
        
        Returns:
            List of error strings
        """
        errors = []
        try:
            while True:
                response = self.visa_session.query(":SYST:ERR:NEXT?")
                error_code, error_msg = response.strip().split(',', 1)
                error_code = int(error_code)
                
                if error_code == 0:
                    break  # No more errors
                
                error_str = f"{error_code}: {error_msg.strip('\"')}"
                errors.append(error_str)
                self.model.system.add_error(error_str)
                
                # Safety: Limit error reading to prevent infinite loop
                if len(errors) > 50:
                    break
                    
        except Exception as e:
            logger.error(f"Error while reading error queue: {e}")
        
        return errors
    
    def clear_errors(self) -> None:
        """Clear instrument error queue."""
        try:
            self.visa_session.write("*CLS")
            self.model.system.clear_errors()
            logger.debug("Error queue cleared")
        except Exception as e:
            logger.warning(f"Failed to clear errors: {e}")
    
    def _check_errors(self) -> None:
        """Check for errors after command execution."""
        now = time.time()
        if now - self._last_error_check > self._error_check_interval:
            errors = self.query_errors()
            if errors:
                logger.warning(f"Instrument errors detected: {errors}")
            self._last_error_check = now
    
    # Status Updates
    
    def _update_system_status(self) -> None:
        """Update system status from instrument."""
        try:
            self.read_stb()
            self.read_oper_cond()
        except Exception as e:
            logger.debug(f"Status update failed: {e}")
    
    def _update_channel_state(self, ch: int) -> None:
        """Update channel state from instrument."""
        try:
            # Read measurements
            self.read_all(ch)
            
            # Read output state
            response = self.visa_session.query(f":OUTP{ch}?")
            output_on = response.strip() == "1"
            self.model.set_output_state(ch, output_on)
            
        except Exception as e:
            logger.debug(f"Channel {ch} state update failed: {e}")
    
    def update_all_measurements(self) -> None:
        """Update measurements for all channels."""
        for ch in range(1, self.num_channels + 1):
            try:
                self.read_all(ch)
            except Exception as e:
                logger.debug(f"Measurement update failed for CH{ch}: {e}")
    
    # Validation Methods
    
    def _validate_channel(self, ch: int) -> None:
        """Validate channel number."""
        if not (1 <= ch <= self.num_channels):
            raise ValueError(f"Invalid channel: {ch}. Must be 1-{self.num_channels}")
    
    def _validate_voltage(self, voltage: float) -> None:
        """Validate voltage value."""
        if not (0 <= voltage <= self.max_voltage):
            raise ValueError(f"Invalid voltage: {voltage}V. Must be 0-{self.max_voltage}V")
    
    def _validate_current(self, current: float) -> None:
        """Validate current value."""
        if not (0 <= current <= self.max_current):
            raise ValueError(f"Invalid current: {current}A. Must be 0-{self.max_current}A")
    
    # Utility Methods
    
    def get_connection_status(self) -> dict:
        """Get connection status information."""
        return {
            'connected': self.model.system.connected,
            'instrument_id': self.model.system.instrument_id,
            'visa_stats': self.visa_session.get_statistics(),
            'error_count': len(self.model.system.error_queue),
            'last_error': self.model.system.last_error
        }
    
    def emergency_stop(self) -> None:
        """Emergency stop - disable all outputs immediately."""
        try:
            self.output_all(False)
            logger.warning("EMERGENCY STOP: All outputs disabled")
        except Exception as e:
            logger.error(f"Emergency stop failed: {e}")
            raise DP2000Error(f"Emergency stop failed: {e}")
    
    def __repr__(self) -> str:
        """String representation."""
        status = "connected" if self.model.system.connected else "disconnected"
        return f"DP2000({self.model.system.instrument_id}, {status})"
