"""
    Lambda function called on the MQTT subscription end to log all events sent and current state of the garage.
"""
import boto3
import time
from datetime import datetime

# Logs will be TTL for 45 days.
days = 45 * 60 * 60 * 24


def lambda_handler(event, context):
    dynamo = boto3.client("dynamodb")
    now = datetime.now()

    item = {
        "received_timestamp": {"S": now.strftime("%m/%d/%Y, %H:%M:%S.%f")
        },
        "timestamp": {
            "S": event["timestamp"]
        },
        "status": {
            "S": event["state"]
        },
        "ttl": {
            "N": int(time.time()) + days
        }
    }

    response = dynamo.put_item(TableName="CarPen9000-EventLog", Item=item, ReturnConsumedCapacity='TOTAL')

    return {
        'statusCode': 200,
        'body': response
    }
