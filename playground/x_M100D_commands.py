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



# add queries or write(s) here
pos = inst.query('1TPU').strip()
print(pos)
