import uos
import machine
import gc

import micropython
import network
import time
import esp


esp.osdebug(None)
gc.collect()


WIFI_SSID = 'workshop'
WIFI_PSWD = '05071175'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(WIFI_SSID, WIFI_PSWD)

while station.isconnected() is False:
    time.sleep(0.1)
    print('.', end='')

print('Connection successful')
print(station.ifconfig())
