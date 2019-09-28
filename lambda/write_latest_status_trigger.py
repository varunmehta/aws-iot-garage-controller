"""
    Using Dynamo triggers on CarPen9000-EventLog, the latest OPEN or CLOSE state of the garage is captured in
    CarPen9000-Latest. Rather than hitting the server to fetch the status, we check this DB to fetch the status

    This lambda function intercepts the events, and pushes the latest data to DynamoDB

"""

import boto3


def lambda_handler(event, context):

    print(len(event['Records']))
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('CarPen9000-Latest')
    response = ''

    for record in event['Records']:
        get_latest_value(record)
        response = table.put_item(get_latest_value(record))

        print("PutItem succeeded:")

    return {
        'statusCode': 200,
    }


def get_latest_value(record):

    item = {
        "status": {
            "S": "latest"
        },
        "timestamp": {
            "S": record['timestamp']
        },
        "last_status": {
            "S": record['status']
        }
    }

    return item
