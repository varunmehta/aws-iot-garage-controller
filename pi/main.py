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

from gpiozero import Motor
from gpiozero import Button
from time import sleep
from datetime import datetime
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# forward is considering closing the garage
# backward is considered opening the garage
motor = Motor(forward=config.PIN_MOTOR_CLOSE, backward=config.PIN_MOTOR_OPEN, pwm=False)
# if the door is open longer than hold time, it'll send an alert.
# to prevent false reads with magnets, the bounce time is 2 seconds
sensor = Button(config.PIN_DOOR_SENSOR, pull_up=True, hold_time=10, bounce_time=5)


def open_too_long_alert():
    """
        When the door is open for too long, you can send an SNS alert.
    """
    lps("LONG_OPEN")


def garage_status(status):
    """
        Send a message to DynamoDB and log the status of the garage door.
        The TTL of the message should be 45 days.
    """
    lps(status)


def garage_opened():
    garage_status("OPEN")


def garage_closed():
    garage_status("CLOSE")


def lps(message):
    """
        L: Log
        P: Print to console
        S: Send to AWS

        This method is supposed to log the message to log4j, print to console (for testing),
        and send the message to be logged as an event. All events are logged.
    """
    now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")

    print('[ ' + now + ' ] ' + message)
    message = '{ "state": "' + message + '", "timestamp": "' + now + '"}'
    message = json.dumps(message)
    message = json.loads(message)
    try:
        client.publishAsync(config.TOPIC_SENSOR, message, 0)
    except AWSIoTMQTTClient.exception.AWSIoTExceptions.publishTimeoutException as e:
        print(e)


def register_door_sensors():
    """
        Magnetic Reed Switch callback methods to be called on change in state.
    """

    sensor.when_activated = garage_opened
    sensor.when_deactivated = garage_closed
    sensor.when_held = open_too_long_alert

    if sensor.is_active | sensor.value == 1:
        lps("Garage door is currently open.")
    elif sensor.is_held | sensor.value == 0:
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
    now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")

    print('[ ' + now + ' ] Sensor state [0: closed, 1: open] = ' + str(sensor.value))

    if garage == "open":
        if sensor.value == 1:
            lps("Garage already open. Nothing to open")
        elif sensor.value == 0:
            lps("Opening the garage...")
            motor.forward()
            sleep(5)
            motor.stop()

    if garage == "close":
        if sensor.value == 0:
            lps("Garage already closed. Nothing to close")
        elif sensor.value == 1:
            lps("Closing the garage...")
            motor.reverse()
            sleep(5)
            motor.stop()

    if garage == "stop":
        lps("Stopping garage door")
        motor.stop()


def reply_garage_status(client, userdata, message):
    """
        Callback method for when the latest status of the garage is requested.
    """
    if sensor.is_active | sensor.value == 1:
        lps("OPEN")
    elif sensor.is_held | sensor.value == 0:
        lps("CLOSED")
    else:
        lps("UNKNOWN")


def handle_subscription(client, userdata, message):
    """
        Call back method called for every subscription

        Where message contains topic and payload.
        Note: client and userdata are pending to be deprecated and should not be depended on.

    """
    # for now printing message, figure out more on payload and play with it.
    lps("Request received on topic: " + str(message.topic) + ", with payload: " + str(message.payload))
    message_data = json.loads(message.payload)
    action = message_data["action"]
    open_close_garage(action)


# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.INFO)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Initialize MQTT client
client = AWSIoTMQTTClient('')

# Configure client endpoint, port information, certs
client.configureEndpoint(config.HOST_NAME, config.HOST_PORT)
client.configureCredentials(config.ROOT_CERT, config.PRIVATE_KEY, config.DEVICE_CERT)
client.configureOfflinePublishQueueing(-1)
client.configureDrainingFrequency(2)
client.configureConnectDisconnectTimeout(10)
client.configureMQTTOperationTimeout(5)
client.subscribe(config.TOPIC_DOOR, 1, handle_subscription)
client.subscribe(config.TOPIC_ASK_SENSOR, 0, reply_garage_status)

# Connect
print('Connecting to endpoint ' + config.HOST_NAME)
client.connect()

register_door_sensors()

"""
For the main method, first register sensors, and then for every subscription, add a call back,
which opens/closes garage.
"""

while True:
    """
        To infinity and beyond!
    """
