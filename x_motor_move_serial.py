import serial
import glob

# ports = glob.glob('/dev/tty[A-Za-z]*')

# print(ports)
# result = []
# for port in ports:
#     # s = serial.Serial(port)
#     # s.close()
#     # result.append(port)
#     try:
#         s = serial.Serial(port)
#         s.close()
#         result.append(port)
#     except (OSError, serial.SerialException):
#         pass
# print(result)
# exit()
import serial.tools.list_ports
print(serial.tools.list_ports.comports())
# exit()
serial = serial.Serial(port='/dev/ttyUSB0',baudrate=921600,bytesize=8,parity='N',stopbits=1,xonxoff=True, timeout=3)
exit()
serial.write('01PA?'.encode('ascii'))
print(serial.read_until(b'\r\n'))