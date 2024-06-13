import kivy
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, ObjectProperty, ListProperty
import time
import math
import os
import subprocess
import socket
import serial



from kivy.config import Config
Config.set("graphics", "width", "500")
Config.set("graphics", "height", "500")
from kivy.core.window import Window
Window.size = (500, 500)
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

try:
    import RPi.GPIO as GPIO
    onPi = 1
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    #if externalshutdown == 1:
    #    GPIO.setup(21, GPIO.IN) # setup GPIO pin 21 as external shutdown pin
except:
    onPi = 0
    externalshutdown = 0
    print("Not running on Raspberry Pi")

class sys:
    ip = "No IP address found..."
    ssid = "No SSID found..."
    CPUTemp = 0
    CPUVolts = 0
    boost = 0
    afr = 0
    screen = 1
    brightness = 0
    shutdownflag = 0

    def setbrightness(self, value):
        sys.brightness = value
        brightset = 'sudo bash -c "echo ' + str(sys.brightness) + ' > /sys/class/backlight/rpi_backlight/brightness"'
        os.system(brightset)

    def loaddata(self):
        f = open("savedata.txt", "r+")
        f.close()

    def savedata(self):
        f = open('savedata.txt', 'r+')
        f.truncate() # wipe everything
        f.write("hello friend")
        f.close()

class MainApp(App):
    def build(self):
        Clock.schedule_interval(self.updatevariables, .1)
        ipAddress = StringProperty()
        WifiNetwork = StringProperty()
        CPUTemp = NumericProperty(0)
        CPUVolts = NumericProperty(0)
        shutdownflag = NumericProperty()
        boost = NumericProperty(0)
        afr = NumericProperty(0)

    def updatevariables(self, *args):
        self.shutdownflag = sys.shutdownflag
        self.get_CPU_info()
        self.get_IP()
        self.get_sensor_data()
        #self.print_data()

    # scheduling functions
    def save(obj):
        sys().savedata()

    def shutdown(obj):
        os.system("sudo shutdown -h now")

    def reboot(obj):
        os.system("sudo reboot")

    def killapp(obj):
        os.system("sudo killall python3") # kills all running processes and threads

    def screenOnOff(obj, action):
        if action == "ON":
            sys.screen = 1
            os.system('sudo bash -c "echo 0 > /sys/class/backlight/rpi_backlight/bl_power"')

        elif action == "OFF":
            sys.screen = 0
            os.system('sudo bash -c "echo 1 > /sys/class/backlight/rpi_backlight/bl_power"')

    def setBrightness(obj, brightvalue):
        brightnesscommand = 'sudo bash -c "echo '+str(brightvalue)+' > /sys/class/backlight/rpi_backlight/brightness"'
        os.system(brightnesscommand)
        sys.brightness = brightvalue

    def get_IP(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            sys.ip = s.getsockname()[0]
        except:
            sys.ip = "No IP address found..."
            #print("Could not get IP")
        try:
            ssidstr = str(subprocess.check_output("iwgetid -r", shell=True))
            sys.ssid = ssidstr[2:-3]
        except:
            sys.ssid = "No SSID found..."
            #print("Could not get SSID")

        self.ipAddress = sys.ip
        self.WifiNetwork = sys.ssid

    def get_sensor_data(self):
        try:
            if(ser.in_waiting > 0):
                line = ser.readline().decode('utf-8').rstrip()
                afr = line.split(',')[0].split('afr:')[1]
                boost = line.split(',')[1].split('boost:')[1]
                
                sys.afr = afr
                sys.boost = boost
        except:
            print("Could not get sensor data")
            sys.boost = 0
            sys.afr = 0

    def get_CPU_info(self):
        try:
            #os.system("cat /sys/class/thermal/thermal_zone0/temp")
            tFile = open("/sys/class/thermal/thermal_zone0/temp")
            temp = float(tFile.read())
            tempC = temp / 1000
            #print(tempC)
            sys.CPUTemp = round(tempC,2)
        except:
            print("Could not get CPU Temp")
            sys.CPUTemp = 0

        self.CPUTemp = sys.CPUTemp

        if (self.CPUTemp > 80):
            print("temp is above 80C")
            print(self.CPUTemp)

    def print_data(self):
        print(f"boost: {sys.boost}, afr: {sys.afr}")



if __name__ == "__main__":
    ser.flush()
    MainApp().run()
