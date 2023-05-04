import pyvisa
from enum import Enum

class Motor:
    # the values for the newport motors:
    SERIAL_BAUD = 921600
    SERIAL_TERMIN = '\r\n'

    def __init__(self, serial_port : str, rm : pyvisa.ResourceManager):
        self._serial_port = serial_port
        self.open_connection(rm)
    
    def open_connection(self, rm):
        """
        rm : pyvisa.ResourceManager object
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

    def read_pos(self, axis : AXES) -> float:
        return self._connection.query(f'1TP{axis.name}').strip()

    def set_absolute_position(self, value : float, axis: AXES):
        self._connection.write(f'1PA{axis.name}{value}')
        self._current_pos[axis] = value

if __name__ == "__main__":
    tt = M100D('ASRL/dev/ttyUSB0::INSTR', pyvisa.ResourceManager())
    print(tt.AXES.U.name)
    print(tt.read_pos(tt.AXES.U))
    tt.set_absolute_position(0.7, tt.AXES.U)
    print(tt.read_pos(tt.AXES.U))