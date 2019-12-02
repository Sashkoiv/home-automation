import machine
import micropython
# # import network
import esp
import gc
import wifi_mngr

esp.osdebug(None)
gc.collect()

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('woke from a deep sleep')
else:
    print('power on or hard reset')

# ---- ADVANCED WAY OF CONNECTION ----- #
wlan = wifi_mngr.get_connection()
if wlan is None:
    print("Could not initialize the network connection.")
    # TODO possibility to reconnect to eliminate endless loop
    while True:
        pass

# ------- OLD WAY OF CONNECTION ------- #
# from config import WIFI_SSID, WIFI_PSWD
# station = network.WLAN(network.STA_IF)

# station.active(True)
# station.connect(WIFI_SSID, WIFI_PSWD)

# while station.isconnected() is False:
#     pass

# print('Connection successful')
# print(station.ifconfig())
