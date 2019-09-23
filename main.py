"""
This is the main garage controller. The features it entails.
 - Open/Close garage on MQTT commands
 - Log status of magnetic switch to garage (this is polling every 10 seconds, we could bring it down to 1 too)
  -- Once the status is detected to be "Open", if more than 2 minutes, send an SNS notification of the garage
     being open for too long.
 - Camera starts recording the moment the switch status is changed to Open
    -- Add motion pi if possible, but too much config to handle.
    -- Can camera always be in preview mode ? and only save to disk when it detects motion ??
 - Alexa ask CarPen to open
 - Alexa ask CarPen to close
 - Alexa ask CarPen the status ~ Return Open or Close

 TODO: Replace all print statements with logs or SNS alerts.

"""
import json
import config
import logging

from enum import Enum
from gpiozero import Motor
from gpiozero import Button
from datetime import datetime
from time import sleep

# from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# forward is considering closing the garage
# backward is considered opening the garage
motor = Motor(forward=config.MOTOR_CLOSE, backward=config.MOTOR_OPEN, pwm=False)
# if the door is open longer than hold time, it'll send an alert.
# to prevent false reads with magnets, the bounce time is 2 seconds
sensor = Button(config.DOOR_SENSOR, pull_up=True, hold_time=10, bounce_time=2)


class Garage(Enum):
    """
        Instead of using if else of "open" or "close", defined a simple enum

        If you want to keep the door partially open for your pet, you can trigger open or close and then stop.

        TODO: Enable pet mode, which opens the garage only for 5 seconds, and vice-versa for close mode.
    """
    OPEN = "open"
    CLOSE = "close"
    STOP = "stop"


# allowed_actions = ['both', 'publish', 'subscribe']

def open_too_long_alert():
    """
        When the door is open for too long, you can send an SNS alert.
    """
    lps("Door open for too long. Do you want to close it ? ")


def garage_status(status):
    """
        Send a message to DynamoDB and log the status of the garage door.
        The TTL of the message should be 45 days.
    """
    lps("Door: " + status)


def garage_opened():
    garage_status(Garage.OPEN)


def garage_closed():
    garage_status(Garage.CLOSE)


def lps(message):
    """
        L: Log
        P: Print to console
        S: Send to AWS

        This method is supposed to log the message to log4j, print to console (for testing),
        and send the message to be logged as an event. All events are logged.
    """
    print(message)


def register_door_sensors():
    """
        Magnetic Reed Switch callback methods to be called on change in state.
    """
    sensor.when_activated = garage_opened
    sensor.when_deactivated = garage_closed
    sensor.when_held = open_too_long_alert

    if sensor.is_held:
        lps("Garage door is currently open.")
    elif sensor.is_active:
        lps("Garage door is currently closed")
    else:
        lps("Garage door status UNKNOWN, please verify manually")


def open_close_garage(garage):
    """
        Meat of the logic to handle garage door open-close.

        Opening or closing of the garage will be triggered based of what the sensor state is. Without the reed switch,
        there is no way for the pi to know if the garage door is opened or closed.

        TODO: test direction with real motor
    """

    if garage.OPEN:
        if sensor.is_held:
            lps("Garage door is already open. Nothing to open")
        elif sensor.is_active:
            lps("Opening the garage...")
            motor.forward()

    if garage.CLOSE:
        if sensor.is_active:
            lps("Garage door is already closed. Nothing to close")
        elif sensor.is_held:
            lps("Closing the garage...")
            motor.reverse()

    if garage.STOP:
        lps("Stopping garage door")
        motor.stop()


def transcribe_message():
    """
        Transcribe the json method via subscription, and open or close garage.
    """

# Configure logging
# logger = logging.getLogger("AWSIoTPythonSDK.core")
# logger.setLevel(logging.INFO)
# streamHandler = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# streamHandler.setFormatter(formatter)
# logger.addHandler(streamHandler)

# Initialize MQTT client
# client = AWSIoTMQTTClient('')

# Configure client endpoint, port information, certs
# client.configureEndpoint(config.HOST_NAME, config.HOST_PORT)
# client.configureCredentials(config.ROOT_CERT, config.PRIVATE_KEY, config.DEVICE_CERT)
# client.configureOfflinePublishQueueing(-1)
# client.configureDrainingFrequency(2)
# client.configureConnectDisconnectTimeout(10)
# client.configureMQTTOperationTimeout(5)
#client.subscribe(topic, 1, myCallbackContainer.messageForward)



# Connect
# print('Connecting to endpoint ' + config.HOST_NAME)


register_door_sensors()

"""
For the main method, first register sensors, and then for every subscription, add a call back, 
which opens/closes garage.  
"""

#while True:


# client.connect()
