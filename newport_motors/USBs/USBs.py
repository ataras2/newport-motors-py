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
        """
        returns a dictionary of the form {serial number -> dev port}
        """
        filt_list = USBs.get_filtered_list(filters)

        port_map = {}
        for connection in filt_list:
            port_map[connection['iSerialNumber']] = connection['devname']
        return port_map
    
    def plug_in_monitor(usb_names : list = []):
        """
        live interaction script that will monitor which devices you plug in and save 
        their serial numbers in a list in order
        """
        prev_status = USBs.discover_all()
        prev_serial_numbers = [d['iSerialNumber'] for d in prev_status]
        new_serial_numbers = []

        i = 0
        while True:
            if usb_names == []:
                prompt = 'Add in a USB and hit enter, or press something else and enter to exit'
            else:
                prompt = f'Plug in {usb_names[i]}'
            s = input(prompt)

            if s != '':
                break

            cur_status = USBs.discover_all()
            cur_serial_numbers = [d['iSerialNumber'] for d in cur_status]

            res = list(set(cur_serial_numbers) - set(prev_serial_numbers))
            assert len(res) == 1
            new_serial_numbers.append(res[0])

            prev_serial_numbers = cur_serial_numbers
            i += 1
            if usb_names != [] and i == len(usb_names):
                break

        return new_serial_numbers




if __name__ == "__main__":
    ### test plug in monitor

    usb_names = [
        "MOTOR_0",
        "MOTOR_1"
    ]
    new = USBs.plug_in_monitor(usb_names)
    assert len(new) == len(usb_names)

    mapping = dict(zip(usb_names, new))

    print(mapping)
    exit()
    ### test remaining

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

