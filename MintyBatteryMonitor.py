#!/usr/bin/python
import time
import os
import signal
from subprocess import check_output
import Adafruit_ADS1x15


# Config
warning = 0
status = 0
debug = 0
iconState = ""
toggleFile = "/home/pi/Mintybatterymonitor/Toggle.txt"
PNGVIEWPATH = "/home/pi/Mintybatterymonitor/Pngview/"
ICONPATH = "/home/pi/Mintybatterymonitor/icons"
CLIPS = 1
REFRESH_RATE = 2
VOLT100 = 1.49  # 4.09
VOLT90 = 1.44   # 4.08
VOLT75 = 1.41   # 3.70
VOLT50 = 1.36   # 3.63
VOLT25 = 1.27   # 3.5
VOLT0 = 1.25    # 3.25
adc = Adafruit_ADS1x15.ADS1015()
#adc = 3.55
GAIN = 1


def changeicon(percent):
    global iconState
    if iconState != percent:
        iconState = percent
        i = 0
        killid = 0
        os.system(PNGVIEWPATH + "/pngview -b 0 -l 3000" + percent + " -x 298 -y 6 " + ICONPATH + "/battery" + percent + ".png &")
        out = check_output("ps aux | grep pngview | awk '{ print $2 }'", shell=True)
        nums = out.split('\n')
        for num in nums:
            i += 1
            if i == 1:
                killid = num
                os.system("sudo kill " + killid)


def endProcess(signalnum=None, handler=None):
    os.system("sudo killall pngview")
    exit(0)


def readVoltage():
    #value = round(adc.read_adc(0, gain=GAIN), 1)
    value = adc.read_adc(0, gain=GAIN)
    #value = "3.4"
    return value


def convertVoltage(sensorValue):
    voltage = float(sensorValue) * (4.09 / 2047.0)
    #voltage = round(voltage), 1)
    #f = open("/home/pi/voltage.txt", 'a+')
    #f.write(str(voltage) + '\n')    
    #print voltage
    return voltage


# Initial Setup

signal.signal(signal.SIGTERM, endProcess)
signal.signal(signal.SIGINT, endProcess)


# Begin Battery Monitoring

os.system(PNGVIEWPATH + "/pngview -b 0 -l 299999 -x 298 -y 6 " + ICONPATH + "/blank.png &")
try:
    with open(toggleFile, 'r') as f:
        output = f.read()
except IOError:
    with open(toggleFile, 'w') as f:
        f.write('1')
    output = '1'
state = int(output)

if state == 1:
    while True:
        try:
            ret1 = readVoltage()
            time.sleep(.4)
            ret2 = readVoltage()
            time.sleep(.4)
            ret3 = readVoltage()
            time.sleep(.4)
            ret4 = (ret1 + ret2 + ret3) / 3
            ret = convertVoltage(ret4)
            if debug == 1:
                print(ret)
            if ret < VOLT0:
                if status != 0:
                    changeicon("0")
                    if CLIPS == 1:
                        os.system("/usr/bin/omxplayer --no-osd --layer 999999  " + ICONPATH + "/lowbattshutdown.mp4 --alpha 160;")
                        os.system("sudo shutdown -h now")
                status = 0
            elif ret < VOLT25:
                if status != 25:
                    changeicon("25")
                    if warning != 1:
                        if CLIPS == 1:
                            os.system("/usr/bin/omxplayer --no-osd --layer 999999  " + ICONPATH + "/lowbattalert.mp4 --alpha 160")
                        warning = 1
                status = 25
            elif ret < VOLT50:
                if status != 50:
                    changeicon("50")
                status = 50
            elif ret < VOLT75:
                if status != 75:
                    changeicon("75")
                status = 75
            elif ret < VOLT90:
                if status != 90:
                    changeicon("90")
                status = 90
            else:
                if status != 100:
		    changeicon("100")
                status = 100
            time.sleep(REFRESH_RATE)
        except IOError:
            #print('No i2c Chip Found!')
            os.system("/home/pi/Mintybatterymonitor/RestartBatteryMonitor.sh > /dev/null 2>&1")
            exit(0)

elif state == 0:
    while True:
        try:
            ret1 = readVoltage()
            time.sleep(.4)
            ret2 = readVoltage()
            time.sleep(.4)
            ret3 = readVoltage()
            time.sleep(.4)
            ret4 = (ret1 + ret2 + ret3) / 3
            ret = convertVoltage(ret4)
            if debug == 1:
                print(ret)
            if ret < VOLT0:
                if status != 0:
                    changeicon("0")
                    if CLIPS == 1:
                        os.system("/usr/bin/omxplayer --no-osd --layer 999999  " + ICONPATH + "/lowbattshutdown.mp4 --alpha 160;")
                        os.system("sudo shutdown -h now")
                    status = 0
            elif ret < VOLT25:
                if status != 25:
                    changeicon("25")
                    if warning != 1:
                        if CLIPS == 1:
                            os.system("/usr/bin/omxplayer --no-osd --layer 999999  " + ICONPATH + "/lowbattalert.mp4 --alpha 160")
                        warning = 1
                status = 25
            elif ret < VOLT50:
                status = 50
            elif ret < VOLT75:
                status = 75
            else:
                status = 100

            time.sleep(REFRESH_RATE)
        except IOError:
            os.system("/home/pi/Mintybatterymonitor/RestartBatteryMonitor.sh > /dev/null 2>&1")
            #print('No i2c Chip Found!')
            exit(0)
