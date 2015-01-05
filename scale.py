#
# by Taka Wang
#

import serial, signal, sys, time

class MT():
    def __init__(self, port = "/dev/ttyUSB0", baudrate = 9600, bytesize = 8, timeout = 5):
        self.port     = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.timeout  = timeout
        try:
            self.serial = serial.Serial(
                self.port, 
                self.baudrate, 
                self.bytesize, 
                parity  = 'N', 
                stopbits = 1, 
                timeout = self.timeout)
            # handle ctrl+c  
            signal.signal(signal.SIGINT, self.__signal_handler)
        except Exception, e:
            print "error open serial port: " + str(e)
            sys.exit(-1)

    def __signal_handler(self, signal, frame):
        if self.serial.isOpen():
            self.serial.close()
            print("Close serial port")
        print("Terminate")
        sys.exit(0)

    def write(self, str, newline=True):
        if newline:
            self.serial.write(str + "\r\n")
        else:
            self.serial.write(str)

    def read(self, trim = True):
        ret = self.serial.readline()
        if trim:
            return ret.rstrip()
        else:
            return ret
    def init(self, kcount=10, zcount=3):
        self.write("@")
        self.write('D "WAIT.."')
        self.write("SIR")
        zero_count, k_count = 0, 0
        while k_count < kcount and zero_count < zcount:
            s = self.read()
            print(s)
            if s.startswith("S S       0.00 g"):
                zero_count = zero_count + 1
            elif s.startswith("S S"):
                k_count = k_count + 1
            else:
                zero_count = 0
                k_count = 0
        self.write("Z") # zero the balance
        self.write("DW")# display show weight
        print("--------------")
    def test(self):
        counter = 0
        self.write("@")
        self.write("Z")
        self.write("SIR")
        while counter < 200:
            str = self.read()
            print(str)
            counter = counter + 1
    def test2(self):
        self.init()
        delta = 0.1
        buf = ""
        should_zero_count = 0
        while True:
            str = self.read()
            if str.startswith("S S"): # stable
                v = float(str[4:14])  # 10 digits
                if v > delta:
                    should_zero_count = 0
                    if str != buf:    # true measurement
                        buf = str
                        print(v)      # shoot from here <-----
                elif v == 0:          # maybe empty
                    buf = ""
                    should_zero_count = 0
                else:
                    should_zero_count = should_zero_count + 1
            else: # Nonstable
                should_zero_count = 0

            if should_zero_count == 3:
                print(".")
                self.write("@")
                self.write("Z") # zero the balance
                self.write("SIR")
                should_zero_count = 0
                buf = ""

if __name__ == '__main__':
    mt = MT()
    mt.test2()


"""
S S       0.00 g
I4 A "1123272678"
S S       0.00 g
S S       0.00 g
Z A
"""