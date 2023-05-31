"Scan for accesspoints and display them sorted by network strength"
# Scan WiFi network and return the list of available access points.
# Each list entry is a tuple with the following items:
# (ssid, bssid, primary_chan, rssi (signal Strength), auth_mode, [ hidden])
import binascii

import network

wlan = network.WLAN(network.STA_IF)
_ = wlan.active(True)
# names of authentication modes - based on esp32 docs - other ports do differ in values
AUTH_MODES = {
    0: "Open",
    1: "WEP",
    2: "WPA-PSK",
    3: "WPA2-PSK",
    4: "WPA/WPA2-PSK",
    5: "WPA2-EAS",
    6: "WPA3-PSK",
    7: "WPA2/WPA3-PSK",
}

wlan.status()


def _authmode(mode: int):
    try:
        return AUTH_MODES[mode]
    except KeyError:
        # handle unknown modes
        return "mode-{}".format(mode)


def _hidden(net: tuple):
    return net[5] if len(net) > 5 else "-"


_networks = wlan.scan()
# sort on signal strength
_networks = sorted(_networks, key=lambda x: x[3], reverse=True)
# define columns and formatting
_f = "{0:<32} {1:>12} {2:>8} {3:>6} {4:<13} {5:>8}"
print(_f.format("SSID", "MAC address", "Channel", "Signal", "Authmode", "Hidden"))
for _net in _networks:
    print(_f.format(_net[0], binascii.hexlify(_net[1]), _net[2], _net[3], _authmode(_net[4]), _hidden(_net)))

del _f, _networks

