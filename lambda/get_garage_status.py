"""
    Using Dynamo triggers on CarPen9000-EventLog, the latest OPEN or CLOSE state of the garage is captured in
    CarPen9000-Latest. Rather than hitting the server to fetch the status, we check this DB to fetch the status

"""

import boto3
import json
from botocore.exceptions import ClientError


def lambda_handler(event, context):
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



def send_message_to_fetch_status(event, context):
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
        'statusCode': 200
    }
