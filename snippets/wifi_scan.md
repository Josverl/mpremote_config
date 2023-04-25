# wifi_scan

## ESP32 WiFi Authentication Modes

The ESP32 chip supports different wifi auth modes for WPA, WPA2 and WPA3, which are reported by the authmode field of the wifi_ap_record_t structure. This structure is returned by the esp_wifi_sta_get_ap_info() function, which can be used to get information about the access point that the ESP32 station is connected to.

The authmode field is an enumeration of type wifi_auth_mode_t, which has the following values and corresponding decimal numbers:

WIFI_AUTH_OPEN: 0, for open system authentication
WIFI_AUTH_WEP: 1, for WEP encryption
WIFI_AUTH_WPA_PSK: 2, for WPA with pre-shared key authentication
WIFI_AUTH_WPA2_PSK: 3, for WPA2 with pre-shared key authentication
WIFI_AUTH_WPA_WPA2_PSK: 4, for WPA/WPA2 mixed mode with pre-shared key authentication
WIFI_AUTH_WPA2_ENTERPRISE: 5, for WPA2 with 802.1X authentication
WIFI_AUTH_WPA3_PSK: 6, for WPA3 with simultaneous authentication of equals (SAE)
WIFI_AUTH_WPA2_WPA3_PSK: 7, for WPA2/WPA3 mixed mode with SAE
You can find more details about the wifi auth modes and the wifi_ap_record_t structure in this document, which is part of the ESP-IDF programming guide.

