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
    logTable = dynamodb.Table('Logs')
    max_key = logTable.item_count('timestamp')
    #timestamp = "01283709222019"
    try:
        response = logTable.get_item(
            Key={
                'timestamp': max_key
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        item = response['Item']
        print("GetItem succeeded:")
        print(json.dumps(item, indent=4, cls=DecimalEncoder))



