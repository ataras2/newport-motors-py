#!/home/adam/miniconda3/envs/motors/bin/python python

import time
import pyvisa


rm = pyvisa.ResourceManager()
print(rm.list_resources())
# exit()
inst = rm.open_resource('ASRL/dev/ttyUSB0::INSTR',
                        baud_rate=921600, 
                        write_termination='\r\n',
                        read_termination='\r\n')
# pos = inst.query('01PA?').strip()
# print(pos)

pos = inst.query('1TPU').strip()
print(pos)

inst.write('1PAU-0.5')

time.sleep(1)

pos = inst.query('1TPU').strip()
print(pos)
