# Fermentation Box
Fermentation box inspired by Noma Guide to Fermentation. 


### Materials:

* 1 insulated box (approx. 60x39x24 cm)
* 1 Raspberry pi 3b+ 
* 1 Raspberry pi power supply
* 1 DHT11 sensor 
* 1 4 relay module (2PH63083A)
* 1 Heating mat 
* 1 Humidifier
* 1 LCD display
* 2 fans, one for the fermentation box and one for cooling hardware box
* 1 USB B to USB micro cable (approx. 2m)
* Wires 
* perforated baking tray (approx. 40x30 cm)
* 4 stands to lift the baking tray off the heating mat

### To be implemented: 

* More efficient control system -> It would be cool with a kalmanfilter or something! 

### Known issues that I do not know how to solve: 
* The humidifier turns on and off with a pulse signal. Sometimes something failes during start up, such that the humidifier is out of sync. \n I think I should replace the humidifier with one that has a real on/off switch and not just a pulse. 


### Modify rc.local to run on start up: 

1. On the Pi edit the rc.local file, which can be accessed using the following command: 

``` sudo nano /etc/rc.local ```

2. Add the file to be executed at the bottom of the page, but before the ```exit 0``` command. Here & is added at the end of the filename, as the script runs continously. 

```python3 /home/pi/FermentationBox/main.py &```

3. Make sure file is executeable. 

```sudo chmod +x /etc/rc.local```

4. Reboot system. 

```sudo reboot```

Now the program should start. 


### Setup:
fritzing file also available. 
Be aware of the gpio pins. The numbering varies between the code and the fritzing sketch.

![alt text](https://github.com/Wedenborg/FermentationBox/blob/main/preliminaryTestSetup.png)
