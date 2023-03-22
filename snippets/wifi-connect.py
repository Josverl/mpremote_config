"Connect to the network (ESP32 / ESP8622)"
import network
import utime

# create station interface - Standard WiFi client
wlan = network.WLAN(network.STA_IF)
# wlan.config(dhcp_hostname="foo-bar-baz")
wlan.active(True)
wlan.connect("IoT", "MicroPython")

# Note that this may take some time, so we need to wait
# Wait 5 sec or until connected
tmo = 50
while not wlan.isconnected():
    utime.sleep_ms(100)
    tmo -= 1
    if tmo == 0:
        break

# check if the station is connected to an AP
if wlan.isconnected():
    print("=== Station Connected to WiFi \n")
    config = wlan.ifconfig()
    print("IP:{0}, Network mask:{1}, Router:{2}, DNS: {3}".format(*config))
else:
    print("!!! Not able to connect to WiFi")
