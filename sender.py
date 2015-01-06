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

def pub(v, params):
    if params[0]:
        params[0].publish(params[1], v)

if __name__ == '__main__':
    #clnt = initMQTT(conf["url"], conf["port"], conf["keepalive"])
    clnt = initMQTT()
    mt = MT()
    mt.run(pub, [clnt, "/scale"])