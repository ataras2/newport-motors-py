import json
from newport_motors.USBs.USBs import USBs
import logging

from newport_motors.Motors.motor import M100D

class Instrument:
    """
    A class to represent a collection of motors that are connected to the same device
    """
    def __init__(self, config_path) -> None:
        """
        config_path: path to the config file for this instrument
        """
        Instrument._validate_config_file(config_path)
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
        """
        For each instrument in the config file, open all the connections and create relevant motor objects
        """
        for name, port in self.name_to_port.items():
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
            if 'motor_type' not in component:
                raise ValueError('Each component must have a motor type')

            if component['motor_type'] in ["M100D"]:
                M100D.validate_config(component["motor_config"])

        # check that all component names are unique:
        names = [component['component'] for component in config]
        if len(names) != len(set(names)):
            raise ValueError('All component names must be unique')


if __name__ == '__main__':
    i = Instrument('InstrumentConfigs/Heimdallr2.json')
    Instrument._validate_config_file('InstrumentConfigs/Heimdallr2.json')
    print(i.name_to_port)