import time
import machine
import ubinascii
from umqttsimple import MQTTClient
from config import SERVER, USER, PASS, PORT, SUB_TOPIC, PUB_TOPIC
from boot import last_message, message_interval, counter


led = machine.Pin(2, machine.Pin.OUT, value = 1)

def sub_cb(topic, msg):
    print((topic, msg))
    if topic == SUB_TOPIC:
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
        SERVER,
        port = PORT,
        user = USER,
        password = PASS)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(PUB_TOPIC)
    print('Connected to %s MQTT broker, subscribed to %s topic' % (SERVER, PUB_TOPIC.decode('utf-8')))
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
            client.publish(PUB_TOPIC, msg)
            last_message = time.time()
            counter += 1
    except OSError as e:
        restart_and_reconnect()