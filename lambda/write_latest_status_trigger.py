"""
    Using Dynamo triggers on CarPen9000-EventLog, the latest OPEN or CLOSE state of the garage is captured in
    CarPen9000-Latest. Rather than hitting the server to fetch the status, we check this DB to fetch the status

    This lambda function intercepts the events, and pushes the latest data to DynamoDB

"""

import boto3
import json


def lambda_handler(event, context):
    print(len(event['Records']))
    print(event['Records'])
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('CarPen9000-Latest')

    for record in event['Records']:
        response = table.delete_item(
            Key={
                'jingo': '1'
            }
        )
        print("Delete Successful :" + str(response))

        item = get_latest_value(record)
        print(item)

        response = table.put_item(Item=item)
        print("PutItem succeeded: " + str(response))

    return {
        'statusCode': 200
    }


def get_latest_value(record):
    """
        Modify incoming record, and add { 'last': 1 } as a value to it

        {'received_timestamp': {'S': '09/28/2019, 21:12:38.687999'}, 'status': {'S': 'CLOSE'}, 'timestamp': {'S': '09/28/2019, 17:12:38.464863'}, 'last': {'N': 1}}

    """

    new_image = record['dynamodb']['NewImage']
    item = {
        'received_timestamp':  new_image["received_timestamp"]["S"],
        'timestamp': new_image["timestamp"]["S"],
        'status': new_image["status"]["S"],
        'jingo': '1'
    }

    return item
