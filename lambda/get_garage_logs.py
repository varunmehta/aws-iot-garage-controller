import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key 
from datetime import datetime


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CarPen9000-EventLog')

def query_table(partition):
    try:
        response = table.query(
            Limit=10, 
            KeyConditionExpression=Key('status').eq(partition),
            ScanIndexForward=False
        )
        return response['Items']
    except ClientError as e:
        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*"
            },
            'body': json.dumps("Error querying table")
        }

def lambda_handler(event, context):
    
    open_list = query_table('OPEN')
    closed_list = query_table('CLOSE')
    long_list = query_table('LONG_OPEN')
    all_queries = open_list + closed_list + long_list
    try:
        sorted_logs = sorted(all_queries, reverse = True, key = lambda i: datetime.strptime(i['received_timestamp'], '%m/%d/%Y, %H:%M:%S.%f'))[:10]
    except (KeyError, ValueError) as e:
        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*"
            },
            'body': {
                'error': str(e),
                'message': 'Key error sorting through logs. received_timestamp was likely not present or formatted correctly'
            }
        }
    
    print('LOGS: {0}'.format(sorted_logs))
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": "*"
        },
        'body': json.dumps(sorted_logs)
    }

