"""
    Using Dynamo triggers on CarPen9000-EventLog, the latest OPEN or CLOSE state of the garage is captured in
    CarPen9000-Latest. Rather than hitting the server to fetch the status, we check this DB to fetch the status

"""

import boto3
import json
from time import sleep
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    send_message_to_fetch_status()

    # THIS IS GODDAMN STUPID INSANE IDEA!!
    # DON'T EVER EVER CALL SLEEP IN A LAMBDA. IT COSTS MONEY!

    # Hoping in 5 seconds we have the latest status from the lambda
    sleep(5)

    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('CarPen9000-Latest')

    try:
        response = table.get_item(
            Key={
                'status': 'latest'
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        item = response['Item']
        return json.dumps(item)


def send_message_to_fetch_status():
    client = boto3.client('iot-data', region_name='us-east-1')
    print("Asking Pi the current garage status")

    body = {"status"}

    # Change topic, qos and payload
    response = client.publish(
        topic='$aws/things/CarPen9000/askSensor',
        qos=1,
        payload=json.dumps(body)
    )

    print(response)
