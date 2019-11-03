https://github.com/Roughtrade/Mintybatterymonitor/blob/master/Circuit.png
# GPI-CASE Batterymonitor!
Script first Published by HoolyHoo (MintyPi Sudomod forum) adapted by Snoopy & Wailer (Retroflag GPi on Discord).

This script is used in conjuction with Adafruit's (or clone) ADS1015/ADS1115 for the Retroflag GPi.
This script will display a battery icon according to battery level and will show a warning video when reaching low level.  Upon critical battery level, the script will show a critical battery level warning video and then introduce a safe shutdown.


#### Automated Software Install
Go to raspberry command prompt or SSH.
Make sure you are in the home directory by typing ```cd ~ ``` and then type:
```
wget https://raw.githubusercontent.com/Roughtrade/Mintybatterymonitor/master/MintyInstall.sh
```
Then type:
```
sudo git clone https://github.com/Roughtrade/Mintybatterymonitor.git
```
Then type:
```
sudo chmod 777 MintyInstall.sh
```
And then type:
```
sudo ./MintyInstall.sh
```
Finally reboot to have it all start on boot with:
```
sudo reboot
```
Error handling Batterymonitor on GPI-CASE:
/opt/retropie/configs/all/emulationstation/es_settings.cfg
change:
<string name="AudioDevice" value="Master" /> or <string name="AudioDevice" value="Digital" /> 
to
<string name="AudioDevice" value="PCM" />
