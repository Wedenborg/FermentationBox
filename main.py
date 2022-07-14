
import os
import glob

import Adafruit_DHT
import RPi.GPIO as GPIO
from datetime import datetime
# Import sleep Module for timing
from time import sleep
import i2c_lcd_driver 
import temperature_sensor_code as stickTemp


 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


# Define pins
BlaaTemp = 22 
BrunTemp = 23
Sensor = 25
Humid = 27
Fan = 24




def setup(BlaaTemp,BrunTemp,Humid,Sensor,Fan):
    # Function that sets up the GPIO pins of heating mat, humidifier and sensor
    # Configures how we are describing our pin numbering
    GPIO.setmode(GPIO.BCM)
    # Disable Warnings
    GPIO.setwarnings(False)

    GPIO.setup(BlaaTemp, GPIO.OUT) # GPIO Assign mode
    GPIO.setup(BrunTemp, GPIO.OUT) # GPIO Assign mode
    GPIO.setup(Humid, GPIO.OUT) # GPIO Assign mode
    GPIO.setup(Sensor, GPIO.OUT) # GPIO Assign mode
    GPIO.setup(Fan, GPIO.OUT) # GPIO Assign mode

    

    return


def heatmatON(temp1,temp2):
    # Function that turns on heating mat
    GPIO.output(temp1, GPIO.LOW)
    GPIO.output(temp2, GPIO.LOW)

    return

def heatmatOFF(temp1,temp2):
    # Function that turns off heating mat
    GPIO.output(temp1, GPIO.HIGH)
    GPIO.output(temp2, GPIO.HIGH)

    return

def signalHumidifier(Humid):
    # Function that turns the humidifier on or off
    GPIO.output(Humid, GPIO.LOW)
    sleep(5)
    GPIO.output(Humid, GPIO.HIGH)
    return

setup(BlaaTemp,BrunTemp,Humid,Sensor,Fan)

K = 60
mylcd = i2c_lcd_driver.lcd()
try:
    humidifier = False
    GPIO.output(Fan, GPIO.LOW) # Turn on fan for better air circulation
    while True:
        
        mylcd.lcd_clear()
        humidity, temperature = Adafruit_DHT.read_retry(11, Sensor)
        tempS = stickTemp.read_temp()
        f = open('/home/emilie/Desktop/Code/FermentationBox/test.csv', 'a')
        f.write(str(tempS) + ',' + str(temperature) + ',' + str(humidity) + ',' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + ','+str(humidifier)+'\n' )
        f.close()
        mylcd.lcd_display_string("Temperature: "+str(tempS),1,0)
        mylcd.lcd_display_string("Humidity: "+str(humidity),2,0)
        humidifier = False


        if tempS < 28:
            heatmatON(BlaaTemp,BrunTemp)
        elif tempS > 34:
            heatmatOFF(BlaaTemp,BrunTemp)
        sleep(1)
        if humidity < 70 and humidifier == False:
            if K >= 60:
                K=0
                signalHumidifier(Humid)
                humidifier = True
                sleep(20)
                signalHumidifier(Humid)

        #elif humidity > 70 and humidifier == True:
        #    signalHumidifier(Humid)
        #    humidifier = False

        sleep(10)
        K += 10

except KeyboardInterrupt:
    GPIO.output(Fan, GPIO.HIGH)
    heatmatOFF(BlaaTemp,BrunTemp)
    if humidity < 70 and humidifier == True:
        signalHumidifier(Humid)

except:
    GPIO.output(Fan, GPIO.HIGH)
    heatmatOFF(BlaaTemp,BrunTemp)
    if humidity < 70 and humidifier == True:
        signalHumidifier(Humid)

