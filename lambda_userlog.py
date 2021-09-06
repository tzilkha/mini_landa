import json
from boto3.dynamodb.conditions import Key
import boto3
import decimal


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.Table('Landa_UserStockCounts')
    data = table.query(
        KeyConditionExpression=Key('username').eq(event['username'])
    )

    if 'Item' in data.keys():
        stocks = data['Item']['num_stocks']['N']
        exists = True
        print('User logged in -', event['username'])
    else:
        stocks = 0
        exists = False
        
        data = table.put_item(
            Item={
                'username': str(event['username']),
                'num_stocks': decimal.Decimal(0)
            } 
        )
        print('Added new user -', event['username'])
    
    return {
        'statusCode': 200,
        'body': json.dumps({'exists':exists, 'stocks':stocks})
    }
