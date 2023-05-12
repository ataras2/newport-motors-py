# newport_motors

## Purpose
This repo contains code used to drive a large project with many newport motors. It is split into the following sub modules:
 - GUI: generic GUI code using `streamlit` that works well with motor alignment projects
 - Mocks: Mock (i.e. simulated) versions of the motors as serial objects, useful for protoyping code before motors ship
 - Motors: Motor driving code for different kinds of newport motors
 - USBs: usb managment code, used to scan USB ports and identify products from a particular manufacturer

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

## Sim mode:
Uses https://github.com/microsoft/pyvisa-mock

## install
To use the sim env with pyvisa mock, you must manually change a line in the pyvisa file to correctly find the mock package. Change line 2820 in `highlevel.py` to use "pyvisa" instead of "pyvisa_". Then, when running in sim, create the resource manager like `pyvisa.ResourceManager(visa_library="@-mock")` and if for real use `pyvisa.ResourceManager(visa_library="@-py")`


