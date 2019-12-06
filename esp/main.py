import time
import machine
import ubinascii
import json
from umqttsimple import MQTTClient
import lm75a


CONFIGFILE = 'config.json'
treshold = 28.0
last_message = 0
message_interval = 5

# recover previous status after reboot
with open('last_status.txt')as f:
    led_v, relay_v = f.read().split('<&>')

# initualize GPIO with before-reboot status
led = machine.Pin(2, machine.Pin.OUT, value=led_v)
relay = machine.Pin(12, machine.Pin.OUT, value=relay_v)

with open(CONFIGFILE) as f:
    raw = json.load(f)
    config = raw['mqtt']
    lm_sensor = [raw['perif']['lm75a']['addr'],
                 raw['intf']['i2c']['scl'],
                 raw['intf']['i2c']['sda']]


def sub_cb(topic: str, msg: str) -> None:
    if topic == config['sub_topic'].encode():

        if msg.decode() == '1':
            led.value(0)
            relay.value(1)
        elif msg.decode() == '0':
            led.value(1)
            relay.value(0)
        else:
            temp = float(msg.decode())
            print(temp)
            if temp < treshold:
                led.value(0)
                relay.value(1)
            elif temp >= treshold:
                led.value(1)
                relay.value(0)
            else:
                print('Incorrect message -> '.format(msg))

    with open('last_status.txt', 'w')as f:
        f.write('{}<&>{}'.format(led.value(), relay.value()))


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
    print('Exception occured \n{}'.format(e))
    restart_and_reconnect()

while True:
    try:
        temp = lm75a.getTemp(*lm_sensor)
    except:
        temp = None

    try:
        client.check_msg()
        # Publish routine
        if (time.time() - last_message) > message_interval:
            if temp:
                msg = str(temp)
            else:
                msg = client.publish(config['pub_topic'], msg)
                last_message = time.time()
    except OSError as e:
        restart_and_reconnect()
