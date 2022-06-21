
import Adafruit_DHT
import RPi.GPIO as GPIO
from datetime import datetime
# Import sleep Module for timing
from time import sleep


# Define pins
BlaaTemp = 22 
BrunTemp = 23
Sensor = 25
Humid = 27



def setup(BlaaTemp,BrunTemp,Humid,Sensor):
    # Function that sets up the GPIO pins of heating mat, humidifier and sensor
    # Configures how we are describing our pin numbering
    GPIO.setmode(GPIO.BCM)
    # Disable Warnings
    GPIO.setwarnings(False)

    GPIO.setup(BlaaTemp, GPIO.OUT) # GPIO Assign mode
    GPIO.setup(BrunTemp, GPIO.OUT) # GPIO Assign mode
    GPIO.setup(Humid, GPIO.OUT) # GPIO Assign mode
    GPIO.setup(Sensor, GPIO.OUT) # GPIO Assign mode

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

setup(BlaaTemp,BrunTemp,Humid,Sensor)

K = 120
try:
    humidifier = False
    while True:
        
        humidity, temperature = Adafruit_DHT.read_retry(11, Sensor)
        f = open('/home/emilie/Desktop/Code/test.csv', 'a')
        f.write(str(temperature) + ',' + str(humidity) + ',' + str(datetime.now().strftime("%H:%M:%S")) + ','+str(humidifier)+'\n')
        f.close()
        humidifier = False


        if temperature < 30:
            heatmatON(BlaaTemp,BrunTemp)
        else:
            heatmatOFF(BlaaTemp,BrunTemp)
        
        if humidity < 70 and humidifier == False:
            if K >= 120:
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
    heatmatOFF(BlaaTemp,BrunTemp)
    if humidity < 70 and humidifier == True:
        signalHumidifier(Humid)

except:
    heatmatOFF(BlaaTemp,BrunTemp)
    if humidity < 70 and humidifier == True:
        signalHumidifier(Humid)

