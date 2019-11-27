import time
import machine
import ubinascii
import yaml
from umqttsimple import MQTTClient
from boot import last_message, message_interval, counter


with open('config.yaml') as f:
    config = yaml.load(f.read())['mqtt']


led = machine.Pin(2, machine.Pin.OUT, value = 1)


def sub_cb(topic, msg):
    print((topic, msg))
    if topic == config['sub_topic']:
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
        port = config['port'],
        user = config['user'],
        password = config['pswd'])
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(config['pub_topic'])
    print('Connected to %s MQTT broker, subscribed to %s topic' % (config['server'], config['pub_topic'].decode('utf-8')))
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
        client.check_msg()
        # Publish routine
        if (time.time() - last_message) > message_interval:
            msg = b'Hello #%d' % counter
            client.publish(config['pub_topic'], msg)
            last_message = time.time()
            counter += 1
    except OSError as e:
        restart_and_reconnect()