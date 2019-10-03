import boto3
from datetime import datetime

'''
Will be called by the Pi to update the Last Known Good State in Dynamo
'''

def lambda_handler(event, context):
    dynamo = boto3.client("dynamodb")
    now = datetime.now()
    
    item = {
        "received_timestamp": { 
            "S": now.strftime("%m/%d/%Y, %H:%M:%S.%f")
        },
        "timestamp": {
          "S": event["timestamp"]  
        },
        "status": {
            "S": event["state"]
        }
    }
    
    response = dynamo.put_item(TableName="CarPen9000-EventLog", Item=item, ReturnConsumedCapacity='TOTAL')
    
    return {
        'statusCode': 200,
        'body': response
    }
