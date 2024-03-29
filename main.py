

import os
import glob
import numpy as np
import Adafruit_DHT
import RPi.GPIO as GPIO
from datetime import datetime
# Import sleep Module for timing
from time import sleep
import csv

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
knap = 5
led = 6

mylcd = i2c_lcd_driver.lcd()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(BlaaTemp, GPIO.OUT) # GPIO Assign mode
GPIO.setup(BrunTemp, GPIO.OUT) # GPIO Assign mode
GPIO.setup(Humid, GPIO.OUT) # GPIO Assign mode
GPIO.setup(Sensor, GPIO.OUT) # GPIO Assign mode
GPIO.setup(Fan, GPIO.OUT) # GPIO Assign mode
GPIO.setup(led, GPIO.OUT) # GPIO Assign mode
GPIO.setup(knap, GPIO.IN) # GPIO Assign mode


 
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
    sleep(1)
    GPIO.output(Humid, GPIO.HIGH)
    return

def writeToDB(path,p):
    dbData =open(path,'r+')
    conn = msql.connect(host=p[0], user=p[1],  
            password=p[2]) #give ur username, password
    try:
        for row in dbData:
            t = row.strip('\n').split(',')
            cursor = conn.cursor()
            cursor.execute("use bnew_dk_db;")
            sql = 'INSERT INTO bnew_dk_db.kojiTable VALUES (%s,%s,%s,%s,%s);'
            cursor.execute(sql,t)
            # the connection is not auto committed by default, so we must commit to save our changes
            conn.commit()
    except Error as e:
        mylcd.lcd_display_string("Error while connecting to MySQL",1)
        mylcd.lcd_display_string(e,2)
    else:
        fileVariable = open(path, 'r+')
        temp = fileVariable.truncate(0)
        fileVariable.close()
    finally:
        dbData.close()
    return
    

def storeData(tempS, temperature, humidity, path):
    line = str(tempS) + "," + str(temperature) + "," + str(humidity) + "," + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "," + str(humidifier)
    out=open(path,"a")
    t = out.write(line+'\n')
    out.close()
    return

p = np.loadtxt("/home/emilie/Desktop/Code/FermentationBox/db.txt", delimiter=",", dtype=str)
path = '/home/emilie/Desktop/Code/FermentationBox/test.txt'


time = datetime.now()
timeOld = time
lastStored = time
humidifier = 0
GPIO.output(Fan, GPIO.LOW) # Turn on fan for better air circulation
heatmatOFF(BlaaTemp,BrunTemp)
mylcd.lcd_display_string("Starting...",1,0)
KorHumid = 1
f = 20
GPIO.output(led,GPIO.LOW) 
while True:
    time = datetime.now()
    
    knapInd = GPIO.input(knap)
    if (knapInd == 1):
        if (KorHumid == 1):
            KorHumid = 0
            GPIO.output(led,GPIO.HIGH)
            if (humidifier == 1):
                humidifier = 0
                signalHumidifier(Humid)
            sleep(3)
        else:
            KorHumid = 1
            GPIO.output(led,GPIO.LOW)
    
        
    tempS = stickTemp.read_temp()
    humidity, temperature = Adafruit_DHT.read_retry(11, Sensor)
    if humidity is not None and temperature is not None:
        mylcd.lcd_clear()
        mylcd.lcd_display_string("Temperature: "+str(tempS),1,0)
        mylcd.lcd_display_string("Humidity: "+str(humidity),2,0)
        mylcd.lcd_display_string(str(knapInd),2,15)

    if abs((time-lastStored).total_seconds()) >= 60:
        storeData(tempS, temperature, humidity,path)
        lastStored = datetime.now()
            
            
    if tempS < 28:
        heatmatON(BlaaTemp,BrunTemp)
    elif tempS > 34:
        heatmatOFF(BlaaTemp,BrunTemp)
            
            
    if humidity < 70 and KorHumid == 1 and humidifier == 0:
        if abs((time-timeOld).total_seconds()) >= 120:
            signalHumidifier(Humid)
            humidifier = 1
            timeOld = time

            if humidity <60:
                f = 40
            else: 
                f = 20

    if KorHumid == 1 and humidifier == 1 and abs((time-timeOld).total_seconds()) >= f:
        signalHumidifier(Humid)
        humidifier = 0
        timeOld = time

    if datetime.now().strftime('%H:%M') == '00:00':
        writeToDB(path,p)


