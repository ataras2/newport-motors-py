import pyvisa

rm = pyvisa.ResourceManager('tests/single_motor.yaml@sim')
print(rm.list_resources())

inst = rm.open_resource('GPIB0::1::INSTR', read_termination='\r\n')
print('here')
print('GPIB0::1::INSTR' in rm.list_resources())

print(inst.query("*IDN?"))