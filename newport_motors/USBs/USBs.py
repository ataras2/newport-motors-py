"""
Module for managing USB connections
"""

import usbinfo


class USBs:
    """
    A class that manages usb connections and can filter particular devices
    Useful to get the mapping serial number -> devname e.g. 12345-> /dev/ttyUSB0

    TODO maybe make singleton?
    """

    def __init__(self) -> None:
        cur_status = USBs.discover_all()
        cur_serial_numbers = [d["iSerialNumber"] for d in cur_status]

        self.serial_numbers = cur_serial_numbers

        print(self.serial_numbers)

    def get_difference(self):
        """
        Update the list of USB serial numbers and return the difference since the last call
        of this function or the constructor
        """
        cur_serial_numbers = [d["iSerialNumber"] for d in USBs.discover_all()]

        diff = list(set(self.serial_numbers) - set(cur_serial_numbers))
        self.serial_numbers = cur_serial_numbers

        print(self.serial_numbers)

        return diff

    @staticmethod
    def discover_all():
        """
        discover all the usb devices
        """
        return usbinfo.usbinfo()

    @staticmethod
    def get_filtered_list(filters: dict[str, str], tty_only: bool = True):
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
                if "tty" not in connection["devname"]:
                    keep = False
            if keep:
                filtered.append(connection)
        return filtered

    @staticmethod
    def compute_serial_to_port_map(filters: dict[str, str]):
        """
        returns a dictionary of the form {serial number -> dev port}
        """
        filt_list = USBs.get_filtered_list(filters)

        port_map = {}
        for connection in filt_list:
            port_map[connection["iSerialNumber"]] = connection["devname"]
        return port_map

    @staticmethod
    def plug_in_monitor(usb_names: list = None):
        """
        live interaction script that will monitor which devices you plug in and save
        their serial numbers in a list in order
        """
        if usb_names is None:
            usb_names = []
        prev_status = USBs.discover_all()
        prev_serial_numbers = [d["iSerialNumber"] for d in prev_status]
        new_serial_numbers = []

        i = 0
        while True:
            if usb_names == []:
                prompt = "Add in a USB and hit enter, or press something else and enter to exit"
            else:
                prompt = f"Plug in {usb_names[i]}"
            s = input(prompt)

            if s != "":
                break

            cur_status = USBs.discover_all()
            cur_serial_numbers = [d["iSerialNumber"] for d in cur_status]

            res = list(set(cur_serial_numbers) - set(prev_serial_numbers))
            assert len(res) == 1
            new_serial_numbers.append(res[0])

            prev_serial_numbers = cur_serial_numbers
            i += 1
            if usb_names != [] and i == len(usb_names):
                break

        return new_serial_numbers
