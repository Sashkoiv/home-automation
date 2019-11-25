import time
import paho.mqtt.client as mqtt
from config import SERVER, USER, PASS, PORT

def on_connect( client, userdata, flags, rc):
    print ("Connected with Code :" +str(rc))
    client.subscribe("Test/#")

def on_message( client, userdata, msg):
    print ( str(msg.payload) )

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(USER, PASS)
client.connect(SERVER, PORT, 60)

# client.loop_forever()
client.loop_start()
time.sleep(1)
while True:
    client.publish("Test","Getting Started with MQTT")
    print ("Message Sent")
    time.sleep(5)

client.loop_stop()
client.disconnect()