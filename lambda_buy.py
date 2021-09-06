import json
import datetime
import boto3
from boto3.dynamodb.conditions import Key
import decimal

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.Table('Landa_Sell')
    response = table.scan()
    
    # Filter possible offers based on who put the and price
    offers = [off for off in response['Items'] if off['username']!=event['username']]
    offers = [(off['id'], float(off['price']), off['username']) for off in offers]
    offers = [off for off in offers if off[1]<=event['price']]
    offers.sort(key=lambda x: x[1])
    
    # No offers, then we create a buy offer
    if len(offers)==0:
        table = dynamodb.Table('Landa_Buy')
        table.put_item(
            Item={
                'id':  str(datetime.datetime.now())+'_'+event['username'],
                'username': event['username'],
                'price': event['price']
            } 
        )
        toreturn = 'Created buy offer for', event['username'], 'at', event['price']

    # We execute the offer and update users
    else:
        # Delete sell offer
        offer = offers[0]
        table = dynamodb.Table('Landa_Sell')
        res = table.delete_item(
            Key={
                'id':  offer[0],
                'username': offer[2]
            } 
        )
        print("Deleted sell offer", offer[0], 'by', offer[2])
        
        # Increment and decrement stock counts
        table = dynamodb.Table('Landa_UserStockCounts')
        response = table.update_item(
            Key={
                'username': event['username']
            },
            UpdateExpression="SET num_stocks = num_stocks + :val",
            ExpressionAttributeValues={
                ':val': decimal.Decimal(1)
            },
            ReturnValues="UPDATED_NEW"
        )
        print("Incremented stock count for", event['username'])
        
        table = dynamodb.Table('Landa_UserStockCounts')
        response = table.update_item(
            Key={
                'username': offer[2]
            },
            UpdateExpression="SET num_stocks = num_stocks - :val",
            ExpressionAttributeValues={
                ':val': decimal.Decimal(1)
            },
            ReturnValues="UPDATED_NEW"
        )
        print("Decremented stock count for", offer[1])
        toreturn = "Executed trade between", offer[1], 'and', event['username']

        # SEND ALERT
    
    return {
        'statusCode': 200,
        'body': toreturn
    }
