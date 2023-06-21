# NewportMotorsPy

This project is **in no way affiliated with Newport**. 

## Purpose
This repo contains code used to drive a large project with many newport motors. It is split into the following sub modules:
 - GUI: generic GUI code using `streamlit` that works well with motor alignment projects
 - Mocks: Mock (i.e. simulated) versions of the motors as serial objects, useful for protoyping code before motors ship
 - Motors: Motor driving code for different kinds of newport motors
 - USBs: usb managment code, used to scan USB ports and identify products from a particular manufacturer

## Installation
This repo is now on PyPi! `pip install newport-motors-py`

## Usage
There are a few different use cases for this package, outlined below.

### Connecting a single motor
To connect a single motor, you use the relevant motor class from `newport_motors.motors`. For example, to connect a `newport_motors.motors.Motor` object, you would do the following:
```python
from newport_motors.motors import Motor

tip_tilt = M100D("ASRL/dev/ttyUSB0::INSTR", pyvisa.ResourceManager(visa_library="@_py"))
print(tip_tilt.read_pos(tip_tilt.AXES.U))
tip_tilt.set_absolute_position(0.0, tip_tilt.AXES.U)
print(tip_tilt.read_pos(tip_tilt.AXES.U))
```

## Simulating a single motor
To simulate a single motor, you use the relevant motor class from `newport_motors.mocks`. For example, to simulate a `newport_motors.motors.Motor` object, you would do the following:
```python
from newport_motors.mocks import Motor
from visa_mock.base.register import register_resource

motor1_port = "MOCK0::mock1::INSTR"
register_resource(motor1_port, Mock_M100D())
```
Then use the motor as above, but with the port as `motor1_port`.

### Connecting multiple motors
To connect multiple motors, you use the `newport_motors.instrument` module. This module contains a class called `Instrument` that is used to connect to multiple motors. To use it, you must first create a config file. This config file is a json file that contains a list of motors and their serial numbers. For example:
```json
[
    {
        "name": "Spherical_1_TipTilt",
        "motor_type": "M100D",
        "motor_config": {
            "orientation": "reversed"
        },
        "serial_number": "A67BVBOJ"
    },
    {
        "name": "Spherical_2_TipTilt",
        "motor_type": "M100D",
        "motor_config": {
            "orientation": "normal"
        },
        "serial_number": "A675RRE6"
    }
]
```

The relevant python code then is
```python
from newport_motors.instrument import Instrument

inst = Instrument("path/to/config.json")
```

Individual motors can still be accessed using `inst.motors["motor_name"]`, but the instrument class also provides some useful methods for accessing multiple motors at once. For example, to move all motors to their home position, you can do
```python
inst.zero_all()
```

### Using a GUI with the motors
The `newport_motors.gui` module contains a generic GUI that can be used to control motors. This uses `streamlit` to create a web app that can be run locally. We provide small blocks to make a larger GUI so that custom projects are easy to create. 


## Linux connection issues
Newport devices did not natively show on ttyUSB* for me. 
Run the following, replacing product id if needed for different products
```
sudo modprobe ftdi_sio vendor=0x104d:3008 product=3008
sudo sh -c 'echo "104d 3008" > /sys/bus/usb-serial/drivers/ftdi_sio/new_id'
```

You can also automated this by altering `~/.bashrc`:
```
# newport motors
if [ ! -d "/sys/bus/usb-serial/drivers/ftdi_sio" ]; then
   sudo modprobe ftdi_sio vendor=0x104d:3008 product=3008
   sudo sh -c 'echo "104d 3008" > /sys/bus/usb-serial/drivers/ftdi_sio/new_id'
fi
```
Since this has `sudo` commands, you will need to enter your password the first time you open a new terminal.

## Sim mode:
Uses https://github.com/microsoft/pyvisa-mock. If you wish to use it you must install it from source (and possibly change `python_requires` in `setup.py`). 

The pyvisa_mock package is defined in this package and is correctly re-exported with `pip install .`. 


