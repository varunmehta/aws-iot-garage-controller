"""
    Using Dynamo triggers on CarPen9000-EventLog, the latest OPEN or CLOSE state of the garage is captured in
    CarPen9000-Latest. Rather than hitting the server to fetch the status, we check this DB to fetch the status

"""

import boto3
import json
from time import sleep
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('CarPen9000-Latest')

    try:
        response = table.scan()
    except ClientError as e:
        print("ERROR")
        print(e.response['Error']['Message'])
    else:
        print(response)
        item_str = response['Items'][0]
        item = json.dumps(item_str)
        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*"
            },
            'body': item
        }


def send_message_to_fetch_status():
    client = boto3.client('iot-data', region_name='us-east-1')
    print("Asking Pi the current garage status")

    body = '{"status"}'

    # Change topic, qos and payload
    response = client.publish(
        topic='$aws/things/CarPen9000/askSensor',
        qos=1,
        payload=json.dumps(body)
    )
