import numpy as np
import os
import glob

import Adafruit_DHT
import RPi.GPIO as GPIO
from datetime import datetime
# Import sleep Module for timing
from time import sleep
import i2c_lcd_driver 
import temperature_sensor_code as stickTemp

import mysql.connector as msql
from mysql.connector import Error


 
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

    GPIO.output(Fan, GPIO.HIGH)
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
# open the sample file used
file = open('db.txt')
# read the content of the file opened
content = file.readlines()
p = content[0].split(",")

try:
    GPIO.output(Fan, GPIO.HIGH)
    mylcd = i2c_lcd_driver.lcd()
    sleep(10)
    mylcd.lcd_display_string("Starting...",1,0)
    sleep(3)
    humidifier = False
    #GPIO.output(Fan, GPIO.LOW) # Turn on fan for better air circulation
    while True:
        
        tempS = stickTemp.read_temp()
        humidity, temperature = Adafruit_DHT.read_retry(11, Sensor)
        mylcd.lcd_clear()
        mylcd.lcd_display_string("Temperature: "+str(tempS),1,0)
        mylcd.lcd_display_string("Humidity: "+str(humidity),2,0)

        with open('test.csv', 'a+') as f:
            f.write(str(tempS) + ',' + str(temperature) + ',' + str(humidity) + ',' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + ','+str(humidifier)+'\n')
            f.close()


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
        if datetime.now().strftime('%H:%M') == '00:00':
            dbData =open('test.csv')
            conn = msql.connect(host=p[0], user=p[1],  
                    password=p[2]) #give ur username, password
            try:
                for row in dbData:
                    t = row.strip('\n').split(',')
                    cursor = conn.cursor()
                    #here %S means string values 
                    cursor.execute("use bnew_dk_db;")
                    sql = 'INSERT INTO bnew_dk_db.kojiTable VALUES (%s,%s,%s,%s,%s);'
                    cursor.execute(sql,t)
                    # the connection is not auto committed by default, so we must commit to save our changes
                    conn.commit()
            except Error as e:
                        print("Error while connecting to MySQL", e)
            else:
                fileVariable = open('test.csv', 'r+')
                fileVariable.truncate(0)
                fileVariable.close()

except KeyboardInterrupt:
    GPIO.output(Fan, GPIO.HIGH)
    mylcd.lcd_clear()
    heatmatOFF(BlaaTemp,BrunTemp)
    if humidity < 70 and humidifier == True:
        signalHumidifier(Humid)

except:
    GPIO.output(Fan, GPIO.HIGH)
    mylcd.lcd_clear()
    heatmatOFF(BlaaTemp,BrunTemp)
    if humidity < 70 and humidifier == True:
        signalHumidifier(Humid)
