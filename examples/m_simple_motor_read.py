from newport_motors.Motors.motor import M100D
from newport_motors.USBs.USBs import USBs
import pyvisa
from pprint import pprint

port = "ASRL/dev/ttyUSB0::INSTR"

mapping = USBs.compute_serial_to_port_map({"iManufacturer": "Newport"})

pprint(mapping)

m = M100D(port, pyvisa.ResourceManager(visa_library="@_py"))

print(f"position: {m.read_pos(M100D.AXES.U)}, {m.read_pos(M100D.AXES.V)}")
