#!/bin/bash

log_file="/home/pi/hotspot_log.txt"

# Logger function
logger() {
    echo "$(date): $1" >> $log_file
}

# Start Hotspot function
start_hotspot() {
    sudo nmcli device wifi hotspot ssid "mindCharger" password "123456789" ifname wlan0
}

# Check WiFi function
check_wifi() {
    for i in {1..10}; do
        result=$(iwgetid | grep "ESSID")
        if [ $? -eq 0 ]; then
            logger "Result: $result"
            sleep 3
            break
        else
            echo "Did not find active connection...$i"
            logger "Did not find active connection...$i"
            if [ $i -ge 9 ]; then
                logger "Starting hotspot..."
                start_hotspot
                break
            fi
            sleep 3
        fi
    done
}

# Run the check_wifi function
check_wifi