from mock_serial import MockSerial

device = MockSerial()
device.open()
device2 = MockSerial()
device2.open()

print(device.port)


import pyvisa

rm = pyvisa.ResourceManager()

print(rm.list_resources())
device_open = rm.open_resource(device.port)




