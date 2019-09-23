'''
This is a skeleton for the simple lambda function that will publish to MQTT.
The config file needs to be configured to include the correct 

'''

import json;
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient;
import config;

def lambda_handler(event, context):
    # Initialize MQTT client
    client = AWSIoTMQTTClient('')
    
    # Configure client endpoint, port information, certs
    # TODO: Need to determine which configurations we will need
    client.configureEndpoint(config.HOST_NAME, config.HOST_PORT)
    client.configureCredentials(config.ROOT_CERT, config.PRIVATE_KEY, config.DEVICE_CERT)
    client.configureOfflinePublishQueueing(-1)
    client.configureDrainingFrequency(2)
    client.configureConnectDisconnectTimeout(10)
    client.configureMQTTOperationTimeout(5)
    
    # Publish to the topic. Event will have been passed from the application and will indicate either open or close
    client.publish(config.SENSOR_TOPIC, event, config.QOS_LEVEL)
    
    return { 
        "statusCode": 200,
        "body": json.dumps(newStatus)
    } 
