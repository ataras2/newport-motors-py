"""
small script used to test the commands from 
https://www.newport.com.cn/mam/celum/celum_assets/resources/CONEX-AGAP_-_Controller_Documentation.pdf?1
"""
import pyvisa


rm = pyvisa.ResourceManager()
print(rm.list_resources())
inst = rm.open_resource('ASRL/dev/ttyUSB0::INSTR',
                        baud_rate=921600, 
                        write_termination='\r\n',
                        read_termination='\r\n')

print(inst.resource_info)

# add queries or write(s) here
pos = inst.query('1TPU').strip()
print(pos)

pos = inst.query('1DBU?').strip()
print(pos)

# deadband settling time, in in units of cycles
pos = inst.query('1DDU?').strip()
print(pos)


# ID is unique to the type of motor but not to the motor itself
pos = inst.query('1ID?').strip()
print(pos)

print(inst.query('1KIU?').strip())
print(inst.query('1KY?').strip())

# lowpass filter freq, Hz
print(inst.query('1LF?').strip())


print(inst.query('1SA?').strip())

# negative software limit
print(inst.query('1SLU?').strip())

# resolution
print(inst.query('1SU?').strip())

# error string info
print(inst.query('1TBA').strip())

# Get last error
print(inst.query('1TE').strip())

# target pos
print(inst.query('1TH').strip())

# cur pos
print(inst.query('1TP').strip())

# positioner error
print(inst.query('1TS').strip())

# revision info
print(inst.query('1VE').strip())


inst2 = rm.open_resource('ASRL/dev/ttyUSB1::INSTR',
                        baud_rate=921600, 
                        write_termination='\r\n',
                        read_termination='\r\n')


pos = inst.query('1VE').strip()
print(pos)
