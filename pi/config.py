# config.py

# AWS IoT endpoint settings
HOST_NAME = "<URL>-ats.iot.us-east-1.amazonaws.com"
HOST_PORT = 8883

# Thing certs & keys
PRIVATE_KEY = "/home/pi/certs9000/private.pem.key"
DEVICE_CERT = "/home/pi/certs9000/certificate.pem.crt"
ROOT_CERT = "/home/pi/certs9000/root-CA.crt"

# Message settings
TOPIC_SENSOR = "$aws/things/CarPen9000/sensor"
TOPIC_ASK_SENSOR = "$aws/things/CarPen9000/askSensor"
TOPIC_DOOR = "$aws/things/CarPen9000/door"
QOS_LEVEL = 1


# GPIO PIN CONFIG
# In the future, fetch this from cloud config, so you can change as needed, without having to change code.
PIN_MOTOR_OPEN = 4
PIN_MOTOR_CLOSE = 14
PIN_DOOR_SENSOR = 21

# RGB LED PINS
PIN_LED_RED = 17
PIN_LED_GREEN = 27
PIN_LED_BLUE = 22