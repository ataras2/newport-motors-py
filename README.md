# newport_motors

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


