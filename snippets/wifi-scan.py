"Scan for accesspoints and display them sorted by network strength"
import binascii

import network

wlan = network.WLAN(network.STA_IF)
_ = wlan.active(True)

AUTH = ["open", "WEP", "WPA-PSK", "WPA2-PSK", "WPA/WPA2-PSK"]

# Scan WiFi network and return the list of available access points.
# Each list entry is a tuple with the following items:
# (ssid, bssid, primary_chan, rssi (signal Strength), auth_mode, auth_mode_string, hidden)
_networks = wlan.scan()
# sort on signal strength
_networks = sorted(_networks, key=lambda x: x[3], reverse=True)
# string to define columns and formatting
# tuple (ssid, bssid, channel, RSSI, security, hidden)
_f = "{0:<32} {1:>8} {2:>8} {3:8} {4:>8}"
print(_f.format("SSID", "mac", "Channel", "Signal", "Authmode", "Hidden"))
for row in _networks:
    print(_f.format(row[0], binascii.hexlify(row[1]), row[2], row[3], AUTH[row[4]]))

del _f
