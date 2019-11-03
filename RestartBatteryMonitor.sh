#!/bin/sh
sudo killall pngview
sudo pkill -f "python /home/pi/Mintybatterymonitor/MintyBatteryMonitor.py"
python /home/pi/Mintybatterymonitor/MintyBatteryMonitor.py > /dev/null 2>&1

