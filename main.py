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
"""
import config
import logging
from gpiozero import Motor
from gpiozero import Button
from datetime import datetime
from time import sleep

# from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# forward is considering closing the garage
# backward is considered opening the garage
motor = Motor(forward=config.MOTOR_CLOSE, backward=config.MOTOR_OPEN, pwm=False)
sensor = Button(config.DOOR_SENSOR, pull_up=True, hold_time=10)
# allowed_actions = ['both', 'publish', 'subscribe']

'''
    When the door is open for too long, you can send an SNS alert.
'''


def open_too_long_alert():
    print("Door open for too long. Do you want to close it ? ")
    return


'''
    Status of the door is open or closed.  
'''


def send_message(status):
    print("Door status changed " + status)


def garage_opened():
    send_message("Opened")
    return


def garage_closed():
    send_message("Closed")
    return


"""
    Meat of the logic to handle garage door open-close.
    Verify against sensor to check if the garage is already open or closed.
"""


def door_sensor():
    sensor.when_activated = garage_opened
    sensor.when_deactivated = garage_closed

    sensor.when_held = open_too_long_alert

    return


def open_close_garage():
    print("Moving the motor forward")
    motor.forward()

    sleep(5)

    print("Moving the motor backward")
    motor.reverse()

    sleep(5)

    print("Stop motor")
    motor.stop()

    return


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


# Connect
# print('Connecting to endpoint ' + config.HOST_NAME)

door_sensor()
open_close_garage()
sleep(60)

# client.connect()
