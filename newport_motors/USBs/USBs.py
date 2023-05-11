import usbinfo
from typing import Union

class USBs:
    """
    A calss that manages usb connections and can filter particular devices
    Useful to get the mapping serial number -> devname e.g. 12345-> /dev/ttyUSB0
    """

    def discover_all():
        return usbinfo.usbinfo()
    
    def get_filtered_list(filters : dict[str : str], tty_only : bool=True):
        """
        get a list of the usb properties for relevant devices

        filters: A dictionary of filters to apply to pick out particular usb devices
                 e.g. {'iManufacturer' : 'Newport'} to only pick out newport devices
        """
        filtered = []
        for connection in USBs.discover_all():
            keep = True
            for key, value in filters.items():
                if connection[key] != value:
                    keep = False
                    break
            if tty_only:
                if 'tty' not in connection["devname"]:
                    keep = False
            if keep:
                filtered.append(connection)
        return filtered
    
    def compute_serial_to_port_map(filters : dict[str : str]):
        filt_list = USBs.get_filtered_list(filters)

        port_map = {}
        for connection in filt_list:
            port_map[connection['iSerialNumber']] = connection['devname']
        return port_map


if __name__ == "__main__":
    from pprint import pprint

    pprint(USBs.discover_all())

    print()

    filt = {
        'iManufacturer' : 'Newport',
        # 'iSerialNumber' : 'A67BVBOJ'
    }

    pprint(USBs.get_filtered_list(filt))

    m = USBs.compute_serial_to_port_map(filt)
    pprint(m)

