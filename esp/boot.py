# This file is executed on every boot (including wake-boot from deepsleep)

# import uos

import ubinascii
import machine
import micropython
import network
import esp
import gc
from config import WIFI_SSID, WIFI_PSWD


esp.osdebug(None)
gc.collect()

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('woke from a deep sleep')
else:
    print('power on or hard reset')

last_message = 0
message_interval = 5
counter = 0

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(WIFI_SSID, WIFI_PSWD)

while station.isconnected() is False:
    pass

print('Connection successful')
print(station.ifconfig())