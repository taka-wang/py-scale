#
# by Taka Wang
#
# ref: http://cs.smith.edu/dftwiki/index.php/PySerial_Simulator

from time import sleep
import random

class Serial():

    ## init(): the constructor.  Many of the arguments have default values
    # and can be skipped when calling the constructor.
    def __init__( self, port='COM1', baudrate = 19200, timeout=1,
                  bytesize = 8, parity = 'N', stopbits = 1, xonxoff=0,
                  rtscts = 0):
        self.name     = port
        self.port     = port
        self.timeout  = timeout
        self.parity   = parity
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.stopbits = stopbits
        self.xonxoff  = xonxoff
        self.rtscts   = rtscts
        self._isOpen  = True
        self._receivedData = ""
        self._data    = []
        self.sir      = False
        random.seed(10) # random seed

    def isOpen( self ):
        return self._isOpen

    def open( self ):
        self._isOpen = True

    def close( self ):
        self._isOpen = False

    def write( self, string ):
        print('[sim]: ' + string.rstrip())
        self._receivedData = string

        if  self._receivedData == "@\r\n":
            self._data.append('I4 A "1123272678"\r\n')
            self.sir = False
        elif self._receivedData == "Z\r\n":
            self._data.append('Z A\r\n')
        elif self._receivedData == "DW\r\n":
            self._data.append('DW A\r\n')
        elif self._receivedData == 'D "WAIT.."\r\n':
            self._data.append('D A\r\n')
        elif self._receivedData == "SIR\r\n":
            self.sir = True
        else:
            pass

    def readline( self ):
        if len(self._data) > 0:
            try:
                ret = self._data.pop(0)
            except Exception, e:
                print(e)
            return ret
        else:
            if self.sir:
                ret = ""
                val = random.uniform(3, 100)

                count = random.randint(20, 60)
                for i in xrange(1, count):
                    self._data.append("S D %10.2f g\r\n" % ((val / count) * i))
                    sleep(0.01)

                for i in range(1, random.randint(40, 100)):
                    self._data.append("S S %10.2f g\r\n" % val)
                    sleep(0.01)

                count = random.randint(20, 60)
                for i in xrange(1, count):
                    self._data.append("S D %10.2f g\r\n" % (val - (val / count) * i))
                    sleep(0.01)

                for i in range(1, random.randint(40, 100)):
                    self._data.append('S S       0.00 g\r\n')
                    sleep(0.01)

                try:
                    ret = self._data.pop(0)
                except Exception, e:
                    print(e)
                return ret
            else:
                return ""

    def __str__( self ):
        return  "Serial<id=0xa81c10, open=%s>( port='%s', baudrate=%d," \
               % ( str(self.isOpen), self.port, self.baudrate ) \
               + " bytesize=%d, parity='%s', stopbits=%d, xonxoff=%d, rtscts=%d)"\
               % ( self.bytesize, self.parity, self.stopbits, self.xonxoff,
                   self.rtscts )