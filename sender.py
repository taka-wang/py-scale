#
# by Taka Wang
#

import paho.mqtt.client as mqtt
import time, ConfigParser
from scale import *

DEBUG = True

def onConnect(client, userdata, rc):
    print("Connected to broker: " + str(rc))

def initMQTT(url = "localhost", port = 1883, keepalive = 60):
    client = mqtt.Client()
    client.on_connect = onConnect
    try:
        client.connect(url, port, keepalive)
        client.loop_start()
        return client
    except Exception, e:
        print(e)
        return None

def run(self, mqttclnt, topic="/scale/"):
    self.init()
    delta = 0.1
    buf = ""
    should_zero_count = 0
    while True:
        str = self.read()
        if str.startswith("S S"): # stable
            v = float(str[4:14])  # 10 digits
            # v range [+inf..delta..0.00..-inf]
            if v > delta:
                should_zero_count = 0
                if str != buf:    # true measurement
                    buf = str
                    
                    if mqttclnt:
                        mqttclnt.publish(topic, v)
            elif v == 0:          # maybe empty
                buf = ""
                should_zero_count = 0
            else:
                should_zero_count = should_zero_count + 1
        else: # Nonstable
            should_zero_count = 0

        if should_zero_count == 3:
            print(".")
            self.write("@")   # reset the balance, SIR cancel
            self.write("Z")   # zero the balance
            self.write("SIR")
            should_zero_count = 0
            buf = ""

if __name__ == '__main__':
    #clnt = initMQTT(conf["url"], conf["port"], conf["keepalive"])
    clnt = initMQTT()
    mt = MT()
    run(mt, clnt, topic="/scale/")