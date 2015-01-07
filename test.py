#
# by Taka Wang
#

DEBUG = True

if DEBUG:
    from simulator import *
else:
    from serial import *

def main():
    serial = Serial(port = "/dev/ttyUSB0", baudrate = 9600, bytesize = 8, parity  = 'N', stopbits = 1, timeout = 5)
    serial.write("@\r\n")           #I4 A "1123272678"
    serial.write("Z\r\n")           #Z A
    serial.write('D "WAIT.."\r\n')  #D A
    serial.write("DW\r\n")          #DW A
    serial.write("SIR\r\n")         #S D       6.35 g
                                    #S S       6.33 g
    count = 0
    while count < 1000:
        s = serial.readline()
        print(s)
        count = count + 1
    if serial.isOpen():
        serial.close()
        print("close")

if __name__ == '__main__':
    main()

