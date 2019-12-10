import time
import machine
import ubinascii
from umqttsimple import MQTTClient


led = machine.Pin(2, machine.Pin.OUT, value=1)
last_message = 0
message_interval = 5
counter = 0
config = {
    "server": "farmer.cloudmqtt.com",
    "port": 11374,
    "user": "npdbwpdg",
    "pswd": "L0JuM560nn71",
    "pub_topic": "workshop",
    "sub_topic": "workshop"
}


def sub_cb(topic: str, msg: str) -> None:
    if topic == config['sub_topic'].encode():

        if msg.decode() == '1':
            led.value(0)
            print('LED ON')
        elif msg.decode() == '0':
            led.value(1)
            print('LED OFF')
        else:
            print('Message is not a command-> {}'.format(msg))


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
        client.check_msg()
        # Publish routine
        if (time.time() - last_message) > message_interval:
            msg = b'{}s passed'.format(counter)
            client.publish(config['pub_topic'], msg)
            last_message = time.time()
            counter += 5
    except OSError as e:
        restart_and_reconnect()
