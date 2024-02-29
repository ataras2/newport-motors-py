#!/home/adam/miniconda3/envs/motors/bin/python python

import time
import pyvisa

resource_manager = pyvisa.ResourceManager()
print(resource_manager.list_resources())

# exit()
inst = resource_manager.open_resource(
    "ASRL/dev/ttyACM0::INSTR",
    baud_rate=921600,
    write_termination="\r\n",
    read_termination="\r\n",
)
# tell target position 
#tar_pos = inst.query("TH?")
cur_pos = inst.query("TP?").strip()
print(f'current position is {cur_pos}')
# jog the motor one way
print(f'jogging motor one way')
inst.write("JA2")
time.sleep(2)
# stop it 
inst.write("ST")
# jog it slowly the other way 
print(f'jogging motor other way')
inst.write("JA-2")
time.sleep(1)
inst.write("ST")
cur_pos = inst.query("TP?").strip()
print(f'current position is {cur_pos}')

# THIS STEP DOESN'T SEEM TO WORK? MAYBE NEDS TO BE IN CL CONFIGURATION?
# SEE https://www.newport.com/mam/celum/celum_assets/resources/Super_Agilis_-_User_s_Manual.pdf?3
print('#RFH: Move to mechanical end of run defined by HT, and take this position as reference.')
inst.write("RFH")

cur_pos = inst.query("TP?").strip()
print(f'current position is {cur_pos} which is now reference position')
