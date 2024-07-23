#!/bin/bash

echo "Starting Hotspot"
sudo nmcli device wifi hotspot ssid "Rpi_mindC" password "123456789" ifname wlan0
echo "Hotspot created"
