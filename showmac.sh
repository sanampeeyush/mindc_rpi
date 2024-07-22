ip link show wlan0 | awk '/ether/ {print $2}'
