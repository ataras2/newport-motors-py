import json
import os


class MotorConfigs:
    SAVE_FOLDER = 'playground'
    """
    Class that deals with storing and retrieving motor configurations.
    Configurations include data on the motor serial numbers, their names and how they should be used.
    """
    def config_to_name(config : dict):
        return f'{config["component"]}_{config["motor"]}_{config["beam"]}'

    def dump_list(configs : list[dict], loc):
        with open(os.path.join(MotorConfigs.SAVE_FOLDER, loc + '.json'), "w") as out_file:
            json.dump(configs, out_file, indent=4)

    def read_list(loc):
        with open(os.path.join(MotorConfigs.SAVE_FOLDER, loc + '.json'), "r") as f:
            configs = json.load(f)
        return configs

if __name__ == "__main__":  
    motor_connection = {
        "internal_name" : "OAP1_Linear_1",
        "serial_number" : "ABCDEF"
    }

    motor_connection2 = {
        "internal_name" : "OAP1_Linear_1",
        "serial_number" : "XYZ"
    }
    motor_connection3 = {
        "internal_name" : "OAP1_TipTilt_1",
        "serial_number" : "XYZ",
        "gravity_dir" : "U"
    }


    configs = [motor_connection, motor_connection2, motor_connection3]

    MotorConfigs.dump_list(configs,'test')


    configs2 = MotorConfigs.read_list('test')
    print(configs2)


