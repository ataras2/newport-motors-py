import usbinfo
import pprint

full_list = usbinfo.usbinfo()
newport_only = []
for connection in full_list:
    if connection['iManufacturer'] == 'Newport' and 'tty' in connection["devname"]:
        newport_only.append(connection)

pprint.pprint(newport_only)
print()


exit()
import pyvisa

rm = pyvisa.ResourceManager()
print(rm.list_resources_info())



exit()
# for this to run correctly, the user needs priveliges
import usb
dev = usb.core.find(idVendor=0x104d, find_all=True)
print(next(dev).iSerialNumber)

exit()

import re
import subprocess

# device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>    \w+:\w+)\s(?P<tag>.+)$", re.I)
df = subprocess.check_output("lsusb -d 104d:3008 -v", shell=True).decode("utf-8")
# print(df)
for i in df.split('\n'):
    if 'Bus 0' in i:
        print(i)
    if 'iSerial' in i:
        print(i.split()[-1])



exit()
import os
from os.path import join

def find_tty_usb(idVendor, idProduct):
    """find_tty_usb('067b', '2302') -> '/dev/ttyUSB0'"""
    # Note: if searching for a lot of pairs, it would be much faster to search
    # for the enitre lot at once instead of going over all the usb devices
    # each time.
    res = []
    for dnbase in os.listdir('/sys/bus/usb/devices'):
        dn = join('/sys/bus/usb/devices', dnbase)
        if not os.path.exists(join(dn, 'idVendor')):
            continue
        idv = open(join(dn, 'idVendor')).read().strip()
        if idv != idVendor:
            continue
        idp = open(join(dn, 'idProduct')).read().strip()
        if idp != idProduct:
            continue
        for subdir in os.listdir(dn):
            if subdir.startswith(dnbase+':'):
                for subsubdir in os.listdir(join(dn, subdir)):
                    if subsubdir.startswith('ttyUSB'):
                        res.append(join('/dev', subsubdir))
    return res

print(find_tty_usb('104d','3008'))

exit()


exit()
import usb
busses = usb.busses()
for bus in busses:
    devices = bus.devices
    for dev in devices:
        print("Device:", dev.filename)
        print("  idVendor: %d (0x%04x)" % (dev.idVendor, dev.idVendor))
        print("  idProduct: %d (0x%04x)" % (dev.idProduct, dev.idProduct))
