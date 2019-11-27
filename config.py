# TODO convert config to yaml or json
# to get rid of need of wifi.dat as extra configuration file
import machine
import ubinascii


# WI-FI setup
WIFI_SSID = 'young-family'
WIFI_PSWD = 'good2best'
AP_SSID = ubinascii.hexlify(machine.unique_id()).decode()
AP_PSWD = '1223334444'
AP_AUTH = 3  # WPA2

# MQTT setup
SERVER = 'farmer.cloudmqtt.com'
USER = 'lxzvqebd'
PASS = 'M0D6C8lfFRGG'
PORT = 12487
SUB_TOPIC = b'Test'
PUB_TOPIC = b'Test'
