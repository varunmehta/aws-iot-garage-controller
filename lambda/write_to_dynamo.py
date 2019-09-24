import json
import boto3
import calendar
import time

'''
Will be called by the Pi to update the Last Known Good State in Dynamo
'''


def lambda_handler(event, context):
    dynamo = boto3.client("dynamodb")
    
    item = {
        "timestamp": { 
            "N": str(calendar.timegm(time.gmtime())) 
        },
        "status": {
            "S": event["garage"]
        }
    }
    
    response = dynamo.put_item(TableName="Logs", Item=item, ReturnConsumedCapacity='TOTAL')
    
    return {
        'statusCode': 200,
        'body': response
    }
