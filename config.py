# config.py

# AWS IoT endpoint settings
HOST_NAME = "your-aws-account-specific-prefix.iot.your-region.amazonaws.com"
HOST_PORT = 8883

# Thing certs & keys
PRIVATE_KEY = "certs/private.pem.key"
DEVICE_CERT = "certs/certificate.pem.crt"
ROOT_CERT = "certs/root-CA.crt"

# Message settings
SENSOR_TOPIC = "garagedoor"
QOS_LEVEL = 0


# GPIO PIN CONFIG
# In the future, fetch this from cloud config, so you can change as needed, without having to change code.
MOTOR_OPEN = 4
MOTOR_CLOSE = 17
DOOR_SENSOR = 24
