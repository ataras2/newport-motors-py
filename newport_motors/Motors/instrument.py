"""
Classes for Instruments
"""

import logging
import json
from typing import Any
import pyvisa

from newport_motors.USBs.USBs import USBs
from newport_motors.Motors.motor import M100D, LS16P, Motor


class Instrument:
    """
    A class to represent a collection of motors that are connected to the same device
    """

    def __init__(self, config_path) -> None:
        """
        config_path: path to the config file for this instrument
        """
        Instrument._validate_config_file(config_path)
        self._config = Instrument._read_motor_config(config_path)
        self._name_to_port_mapping = self._name_to_port()
        self._motors = self._open_conncetions()

    def zero_all(self):
        """
        Zero all the motors
        """
        for name, motor in self._motors.items():
            motor.set_to_zero()

    def _name_to_port(self):
        filt = {"iManufacturer": "Newport"}
        serial_to_port = USBs.compute_serial_to_port_map(filt)
        name_to_port = {}
        for mapping in self._config:
            serial = mapping["serial_number"]
            logging.info(f"Searching for serial number {serial}")
            try:
                name = mapping["name"]
                port = serial_to_port[serial]
                name_to_port[name] = port
            except KeyError:
                logging.warning(f" Could not find serial number {serial} in the USBs")
        return name_to_port

    @property
    def name_to_port(self):
        """
        The dictionary that maps the name of the motor to the port it is connected to
        """
        return self._name_to_port_mapping

    def __getitem__(self, key) -> Motor:
        """
        Get a motor by name
        """
        if key not in self._motors:
            raise KeyError(f"Could not find motor {key}")
        return self._motors[key]

    @property
    def motors(self):
        """
        the motors of the string
        """
        return self._motors

    def _open_conncetions(self):
        """
        For each instrument in the config file, open all the connections and create relevant
        motor objects
        """
        resource_manager = pyvisa.ResourceManager(visa_library="@_py")

        motors = {}

        for component in self._config:
            visa_port = f"ASRL{self._name_to_port_mapping[component['name']]}::INSTR"
            if component["motor_type"] == "M100D":
                motors[component["name"]] = M100D(
                    visa_port, resource_manager, **component["motor_config"]
                )
            elif component["motor_type"] == "LS16P":
                motors[component["name"]] = LS16P(visa_port, resource_manager)

        return motors

    @classmethod
    def _read_motor_config(cls, config_path):
        """
        Read the json config file and return the config dictionary
        """
        with open(config_path, "r", encoding="utf-8") as file:
            config = json.load(file)
        return config

    @classmethod
    def _validate_config_file(cls, config_path):
        """
        Reads in the config file and verifies that it is valid
        """
        with open(config_path, "r", encoding="utf-8") as file:
            config = json.load(file)

        for component in config:
            if "name" not in component:
                raise ValueError("Each component must have a name")
            if "serial_number" not in component:
                raise ValueError("Each component must have a serial number")
            if "motor_type" not in component:
                raise ValueError("Each component must have a motor type")

            if component["motor_type"] in ["M100D"]:
                M100D.validate_config(component["motor_config"])

        # check that all component names are unique:
        names = [component["name"] for component in config]
        if len(names) != len(set(names)):
            raise ValueError("All component names must be unique")

    @classmethod
    def _create_config_with_plugin(cls, config_path):
        """
        Using a USB monitor, create a config file with all the motors that are
        connected one at a time

        config_path: path for where to save the resulting config file
        """
        USBs.plug_in_monitor()


if __name__ == "__main__":
    i = Instrument("InstrumentConfigs/Heimdallr_tt_only.json")
    print(i.name_to_port)

    # M100D("ASRL/dev/ttyUSB1::INSTR", pyvisa.ResourceManager("@_py"))

    print(i.motors["Spherical_1_TipTilt"])
    print(i["Spherical_1_TipTilt"]._is_reversed)

    i.zero_all()

    # # print(i["Spherical_1_TipTilt"]._is_reversed)
    # i["Spherical_1_TipTilt"].set_to_zero()
    # import time

    # time.sleep(3)
    # i["Spherical_1_TipTilt"].set_absolute_position(0.5, M100D.AXES.U)
