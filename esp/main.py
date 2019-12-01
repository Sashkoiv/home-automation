import time
import machine
import ubinascii
# import yaml
import json
from umqttsimple import MQTTClient
import lm75a
from boot import last_message, message_interval, counter

CONFIGFILE = 'config.json'


# with open('CONFIG') as f:
#     config = yaml.load(f.read())['mqtt']
with open(CONFIGFILE) as f:
    config = json.load(f)['mqtt']


led = machine.Pin(2, machine.Pin.OUT, value=1)


def sub_cb(topic, msg):
    if topic == config['sub_topic'].encode():
        # led.value(not p.value())
        if msg == b'1':
            led.value(0)
        elif msg == b'0':
            led.value(1)
        else:
            print('message unknown')


def connect_and_subscribe():
    client_id = ubinascii.hexlify(machine.unique_id())
    client = MQTTClient(
        client_id,
        config['server'],
        port=config['port'],
        user=config['user'],
        password=config['pswd'])
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(config['pub_topic'])
    print('Connected to %s MQTT broker, subscribed to %s topic' %
          (config['server'], config['pub_topic']))
    return client


def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()


try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

while True:
    try:
        temp = lm75a.getTemp(72, 22, 21)
    except:
        temp = -100500

    try:
        client.check_msg()
        # Publish routine
        if (time.time() - last_message) > message_interval:

            msg = 'msg #{}\ntemp {}'.format(counter, temp)

            client.publish(config['pub_topic'], msg)
            last_message = time.time()
            counter += 1
    except OSError as e:
        restart_and_reconnect()
