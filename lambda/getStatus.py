import json
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# TODO implement

def lambda_handler(event, context):
    class DecimalEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, decimal.Decimal):
                if o % 1 > 0:
                    return float(o)
                else:
                    return int(o)
            return super(DecimalEncoder, self).default(o)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Logs')
    fe = Key('timestamp').gt(0)
    pe = "#ts,#st"
    ean = { "#ts": "timestamp", "#st" : "status"}
    
    response = table.scan(
        FilterExpression=fe,
        ProjectionExpression=pe,
        ExpressionAttributeNames=ean
    )
    while 'LastEvaluatedKey' in response:
        response = table.scan(
            ProjectionExpression=pe,
            FilterExpression=fe,
            ExpressionAttributeNames=ean,
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        
    currentStatus = max(response['Items'], key=lambda Item: Item['timestamp'])
    print(currentStatus)


        


