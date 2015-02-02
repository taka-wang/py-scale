#
# by Taka Wang
#

import paho.mqtt.client as mqtt
import time, ConfigParser
from scale import *
zero_count = 0

def onConnect(client, userdata, rc):
    """MQTT onConnect handler"""
    print("Connected to broker: " + str(rc))

def initMQTT(url = "localhost", port = 1883, keepalive = 60):
    """Init MQTT connection"""
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
    """MQTT publish handler
    Publish scale value via mqtt
    """
    if params[0]:
        if zero_count < 2: #prevent too much zero feedback
            params[0].publish(params[1], v)
        if v != 0: #reset zero count for actual values
            zero_count = 0
            print(v)
        else:
            zero_count = zero_count + 1

def init():
    """Read config file"""
    ret = {}
    config = ConfigParser.ConfigParser()
    config.read("config")
    ret["url"]           = config.get('MQTT', 'url')
    ret["port"]          = int(config.get('MQTT', 'port'))
    ret["keepalive"]     = int(config.get('MQTT', 'keepalive'))
    ret["topic"]         = config.get('MT', 'topic')
    ret["debug"] = True if int(config.get('MT', 'debug')) == 1 else False
    return ret

if __name__ == '__main__':
    conf = init()
    clnt = initMQTT(conf["url"], conf["port"], conf["keepalive"])
    mt = MT(debug=conf["debug"])
    mt.run(pub, [clnt, conf["topic"]])