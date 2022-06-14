
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

def signalHumidifier(humid):
    # Function that turns the humidifier on or off
    GPIO.output(Humid, GPIO.LOW)
    GPIO.output(Humid, GPIO.HIGH)
    return



try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(11, Sensor)
        f = open('/home/emilie/Desktop/Code/test.csv', 'a')
        f.write(str(temperature) + ',' + str(humidity) + ',' + str(datetime.now().strftime("%H:%M:%S")) + '\n')
        f.close()
        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))

        if temperature < 30:
            heatmatON(BlaaTemp,BrunTemp)
        else:
            heatmatOFF(BlaaTemp,BrunTemp)
        
        if humidity < 70:
            signalHumidifier(Humid)
        else:
            signalHumidifier(Humid)

        sleep(60)

except:
    heatmatOFF(BlaaTemp,BrunTemp)
    if humidity < 70:
        signalHumidifier(Humid)
