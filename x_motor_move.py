#!/home/adam/miniconda3/envs/motors/bin/python python

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