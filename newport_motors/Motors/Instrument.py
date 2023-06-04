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
            'iManufacturer' : 'Newport'
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

    @classmethod
    def _validate_config_file(cls, config_path):
        """
        Reads in the config file and verifies that it is valid
        """
        with open(config_path, 'r') as f:
            config = json.load(f)
        

        for component in config:
            if 'component' not in component:
                raise ValueError('Each component must have a name')
            if 'serial_number' not in component:
                raise ValueError('Each component must have a serial number')
            if 'orientation' not in component:
                raise ValueError('Each component must have a orientation flag')
            
            if component['orientation'] not in ["normal", "reversed"]:
                raise ValueError('The orientation flag must be one of "normal", "reversed"')



if __name__ == '__main__':
    i = Instrument('InstrumentConfigs/Heimdallr2.json')
    Instrument._validate_config_file('InstrumentConfigs/Heimdallr2.json')
    print(i.name_to_port)