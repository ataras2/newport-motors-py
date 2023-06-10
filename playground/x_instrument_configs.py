import json
import os

from newport_motors.Motors.motor import M100D


class MotorConfigs:
    SAVE_FOLDER = "playground"
    """
    Class that deals with storing and retrieving motor configurations.
    Configurations include data on the motor serial numbers, their names and how they should be used.
    """

    def config_to_name(config: dict):
        return f'{config["component"]}_{config["motor"]}_{config["beam"]}'

    def dump_list(configs: list[dict], loc):
        with open(
            os.path.join(MotorConfigs.SAVE_FOLDER, loc + ".json"), "w"
        ) as out_file:
            json.dump(configs, out_file, indent=4)

    def read_list(loc):
        with open(os.path.join(MotorConfigs.SAVE_FOLDER, loc + ".json"), "r") as f:
            configs = json.load(f)
        return configs


if __name__ == "__main__":
    motor_connection = {
        "internal_name": "test",
        # "motor_type": M100D,
        "serial_number": "ABCDEF",
    }

    configs = [motor_connection]

    MotorConfigs.dump_list(configs, "test")

    configs2 = MotorConfigs.read_list("test")
    print(configs2)
