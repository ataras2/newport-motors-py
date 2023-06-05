"""
Module for the newport motors.
"""

from enum import Enum
import logging
import parse

import pyvisa


class Motor:
    """
    Base class for all the newport motors
    """

    # The serial config for the newport motors:
    SERIAL_BAUD = 921600
    SERIAL_TERMIN = "\r\n"

    def __init__(
        self, serial_port: str, resource_manager: pyvisa.ResourceManager, **kwargs
    ):
        self._serial_port = serial_port
        self.open_connection(resource_manager)
        self._verify_valid_connection()

    def open_connection(self, resource_manager: pyvisa.ResourceManager):
        """
        resource_manager : pyvisa.ResourceManager object (to avoid constructing it many times)
        """
        self._connection = resource_manager.open_resource(
            self._serial_port,
            baud_rate=self.SERIAL_BAUD,
            write_termination=self.SERIAL_TERMIN,
            read_termination=self.SERIAL_TERMIN,
        )

    def _verify_valid_connection(self):
        raise NotImplementedError()

    def write_str(self, str_to_write):
        """
        Write a string through serial and do not expect anything to be returned
        """
        self._connection.write(str_to_write)

    def query_str(self, str_to_write):
        """
        Send a query through serial and return the response
        """
        return_str = self._connection.query(str_to_write).strip()
        return return_str

    def set_to_zero(self):
        """
        Set the motor to the zero position
        """
        raise NotImplementedError()

    @classmethod
    def validate_config(cls, config):
        """
        Validate the config dictionary for the motor
        """
        if "orientation" not in config:
            raise KeyError("orientation not in config")


class M100D(Motor):
    """
    A tip tilt motor driver class
    https://www.newport.com.cn/p/CONEX-AG-M100D
    """

    AXES = Enum("AXES", ["U", "V"])
    HW_BOUNDS = {AXES.U: [-0.75, 0.75], AXES.V: [-0.75, 0.75]}

    def __init__(
        self, serial_port, resource_manager: pyvisa.ResourceManager, **kwargs
    ) -> None:
        super().__init__(serial_port, resource_manager)
        self._current_pos = {self.AXES.U: 0.0, self.AXES.V: 0.0}
        # TODO: this needs some thinking about how to implement so that the external interface doesn't notice
        if "orientation" in kwargs:
            self._is_reversed = kwargs["orientation"] == "reversed"

    def _verify_valid_connection(self):
        """
        Verify that the serial connection opened by the class is indeed to to a NEWPORT M100D
        """
        id_number = self._connection.query("1ID?").strip()  #
        assert "M100D" in id_number

    @property
    def get_current_pos(self):
        """
        Return the current position of the motor in degrees
        """
        return [self._current_pos[ax] for ax in M100D.AXES]

    def set_to_zero(self):
        """
        Set all the motor axes positions to zero
        """
        for axis in self.AXES:
            self.set_absolute_position(0.0, axis)

    def read_pos(self, axis: AXES) -> float:
        """
        Read the position of a given axis.

        Parameters:
            axis (M100D.AXES) : the axis to read from

        Returns:
            position (float) : the position of the axis in degrees
        """
        return_str = self._connection.query(f"1TP{axis.name}").strip()
        subset = parse.parse("{}" + f"TP{axis.name}" + "{}", return_str)
        if subset is not None:
            return float(subset[1])
        raise ValueError(f"Could not parse {return_str}")

    def set_absolute_position(self, value: float, axis: AXES):
        """
        Set the absolute position of the motor in a given axis

        Parameters:
            value (float) : The new position in degrees
            axis (M100D.AXES) : the axis to set
        """
        str_to_write = f"1PA{axis.name}{value}"
        logging.info(f"sending {str_to_write}")
        self._connection.write(str_to_write)
        self._current_pos[axis] = value


class LS16P(Motor):
    """
    A linear motor driver class
    https://www.newport.com/p/CONEX-SAG-LS16P
    """

    HW_BOUNDS = [-8.0, 8.0]

    def __init__(self, serial_port: str, resource_manager: pyvisa.ResourceManager):
        super().__init__(serial_port, resource_manager)
        self._current_pos = 0.0

    def _verify_valid_connection(self):
        """
        Verify that the serial connection opened by the class is indeed to to a NEWPORT LS16P
        """
        id_number = self._connection.query("1ID?").strip()
        assert "LS16P" in id_number

    def set_absolute_position(self, value: float):
        """
        Set the absolute position of the motor

        Parameters:
            value (float) : The new position in mm
        """
        str_to_write = f"1PA{value}"
        self._connection.write(str_to_write)
        self._current_pos = value

    def read_pos(self) -> float:
        """
        Set the absolute position of the motor

        Returns:
            value (float) : The new position in mm
        """
        return_str = self._connection.query("1TP").strip()
        subset = parse.parse("{}TP{}", return_str)
        if subset is not None:
            return float(subset[1])
        raise ValueError(f"Could not parse {return_str}")

    @property
    def get_current_pos(self):
        """
        Return the software internal position of the motor
        """
        return self._current_pos


if __name__ == "__main__":
    # example code:
    # Open a connection to a M100D on ttyUSB0,
    # verify the AXES attributes, read a position and set a position
    tt = M100D("ASRL/dev/ttyUSB0::INSTR", pyvisa.ResourceManager(visa_library="@_py"))
    print(tt.AXES.U.name)
    print(tt.read_pos(tt.AXES.U))
    tt.set_absolute_position(0.0, tt.AXES.U)
    print(tt.read_pos(tt.AXES.U))
