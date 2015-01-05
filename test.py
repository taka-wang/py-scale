import serial
#ser = serial.Serial(0)
#serialport = Serial('/dev/ttyS0', baudrate=9600, bytesize=SEVENBITS, parity=PARITY_EVEN, stopbits=STOPBITS_ONE)
serialport = serial.Serial(0, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=5)
print("Port open")
serialport.write('SIR\r\n')
s = serialport.read(100)
if serialport.isOpen():
    serialport.close()
    print("close")