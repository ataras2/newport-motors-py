import json
from newport_motors.USBs.USBs import USBs
import logging

class Instrument:
    """
    A collection of motors
    """
    def __init__(self, config_path) -> None:
        self._name_to_port_mapping = self._name_to_port(config_path)
    
    def _name_to_port(self,config_path):
        motor_map = Instrument._read_motor_mapping(config_path)
        filt = {
            'iManufacturer' : 'Newport',
            # 'iSerialNumber' : 'A67BVBOJ'
        }
        serial_to_port = USBs.compute_serial_to_port_map(filt)
        name_to_port = {}
        for mapping in motor_map:
            try:
                serial = mapping['serial_number']
                name = mapping['component']
                port = serial_to_port[serial]
                name_to_port[name] = port
            except KeyError:
                logging.warn(f' Could not find serial number {serial} in the USBs')
        return name_to_port
    
    @property
    def name_to_port(self):
        return self._name_to_port_mapping

    def open_conncetions(self):
        pass

    def _read_motor_mapping(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config



if __name__ == '__main__':
    i = Instrument('InstrumentConfigs/Heimdallr2.json')
    print(i.name_to_port)