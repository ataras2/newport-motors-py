from newport_motors.USBs.USBs import USBs
from pprint import pprint

u = USBs()

print(u.get_difference())

input("Add a USB and hit enter...")

print(u.get_difference())

### test plug in monitor

# usbs = ["MOTOR_0", "MOTOR_1"]
# new = USBs.plug_in_monitor(usbs)
# assert len(new) == len(usbs)

# mapping = dict(zip(usbs, new))

# print(mapping)
# exit()
### test remaining

# pprint(USBs.discover_all())

# print()

# filt = {
#     "iManufacturer": "Newport",
#     # 'iSerialNumber' : 'A67BVBOJ'
# }

# pprint(USBs.get_filtered_list(filt))

# m = USBs.compute_serial_to_port_map(filt)
# pprint(m)