# Raspberry Pi

The code that runs on the Raspberry Pi resides here. For hardware setup, please refer the home page of this project. It lays out the connection diagram and overall architecture diagram of the application.

## config.py

Change topic names, location of certificates and GPIO pins if you rewire your garage.

## main.py

The main script, that is run on server start and is running for infinity. To get more details, read the code, have added comments to most of the functions.

## Deploy on the Pi

 * Setup Pi. This is well documented on https://raspberrypi.org
 * Enable GPIO
 * Switch locale, time zone, setup wifi
 * Install needed packages via pip3 as specified in requirements.txt
 * Checkout code to pi
 * Modify config.py as appropriate to your setup.

## Run script on startup

The main.py is started on server startup.

```
$ crontab -e
```

Add the following line to the crontab file. There is a 60 seconds delay in starting the script, to ensure the IP has be procured and set, and all system services have been completely initialized.

```
# Command to start the program on system startup.
@reboot python3 sleep 60 && /home/pi/aws-iot-garage-controller/pi/main.py >> ~/aws-iot-garage-controller/pi/logs 2>&1
```
