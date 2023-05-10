import pyvisa
from enum import Enum
import parse

class Motor:
    # the values for the newport motors:
    SERIAL_BAUD = 921600
    SERIAL_TERMIN = '\r\n'

    def __init__(self, serial_port : str, rm : pyvisa.ResourceManager):
        self._serial_port = serial_port
        self.open_connection(rm)
    
    def open_connection(self, rm : pyvisa.ResourceManager):
        """
        rm : pyvisa.ResourceManager object (to avoid constructing it many times)
        """
        self._connection = rm.open_resource(self._serial_port,
                                            baud_rate=self.SERIAL_BAUD, 
                                            write_termination=self.SERIAL_TERMIN,
                                            read_termination=self.SERIAL_TERMIN)


class M100D(Motor):
    AXES = Enum('AXES', ['U', 'V'])
    BOUNDS = {
        AXES.U : [-0.75, 0.75],
        AXES.V : [-0.75, 0.75]
    }

    def __init__(self, serial_port, rm : pyvisa.ResourceManager) -> None:
        super().__init__(serial_port, rm)
        self._current_pos = {
            self.AXES.U : 0.0,
            self.AXES.V : 0.0 
        }

    
    def get_current_pos(self):
        return [self._current_pos[ax] for ax in M100D.AXES]

    def set_to_zero(self):
        """
        Set all the motor axes positions to zero
        """
        for ax in self.AXES:
            self.set_absolute_position(0., ax)

    def read_pos(self, axis : AXES) -> float:
        """
        Read the position of a given axis. 

        Parameters:
            axis (M100D.AXES) : the axis to read from
        
        Returns:
            position (float) : the position of the axis in degrees
        """
        return_str = self._connection.query(f'1TP{axis.name}').strip()
        return float(parse.parse('{}TPU{}',return_str)[1])

    def set_absolute_position(self, value : float, axis: AXES):
        """
        Set the absolute position of the motor in a given axis

        Parameters:
            value (float) : The new position in degrees
            axis (M100D.AXES) : the axis to set
        """
        str_to_write = f'1PA{axis.name}{value}'
        print("sending", str_to_write)
        self._connection.write(str_to_write)
        self._current_pos[axis] = value
        print(f'running set abs pos, is now {self._current_pos}')


if __name__ == "__main__":
    # example code:
    # Open a connection to a M100D on ttyUSB0,
    # verify the AXES attributes, read a position and set a position
    tt = M100D('ASRL/dev/ttyUSB0::INSTR', pyvisa.ResourceManager())
    print(tt.AXES.U.name)
    print(tt.read_pos(tt.AXES.U))
    tt.set_absolute_position(0., tt.AXES.U)
    print(tt.read_pos(tt.AXES.U))