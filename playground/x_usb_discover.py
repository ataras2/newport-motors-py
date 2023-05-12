import usbinfo
import pprint

full_list = usbinfo.usbinfo()
newport_only = []
for connection in full_list:
    if connection['iManufacturer'] == 'Newport' and 'tty' in connection["devname"]:
        newport_only.append(connection)

pprint.pprint(newport_only)
print()


