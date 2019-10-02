"""
    Open Sesame Lambda which posts a message to MQTT queue to open, close or stop the garage motor.
"""

import boto3


def lambda_handler(event, context):
    print("Lambda Invoked")
    client = boto3.client('iot-data', region_name='us-east-1')
    print(event['body'])

    # Change topic, qos and payload
    response = client.publish(
        topic='$aws/things/CarPen9000/door',
        qos=1,
        payload=event['body']
    )

    print("Response")
    print(response)

    return {
        'statusCode': 200,
	'headers': {
            "Access-Control-Allow-Origin": "*"
        }	
    }
