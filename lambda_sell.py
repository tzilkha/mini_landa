import json
import datetime
import boto3
from boto3.dynamodb.conditions import Key
import decimal

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    
    # First we check if we can create a sell offer
    table = dynamodb.Table('Landa_Sell')
    response = table.scan()
    my_offers = len([off for off in response['Items'] if off['username']==event['username']])
    
    table = dynamodb.Table('Landa_UserStockCounts')
    data = table.query(
        KeyConditionExpression=Key('username').eq(event['username'])
    )
    stocks = data['Item']['num_stocks']['N']
    
    # Check if were selling too many already
    if stocks-offers==0:
        print("Invalid sell, not more stocks to sell")
        return {
            'statusCode': 200,
            'body': 'Invalid sell, no more stocks to sell, either user has no stocks or they are all under sell orders'
        }
    
    # We have a stock to sell
    table = dynamodb.Table('Landa_Buy')
    response = table.scan()
    
    # Filter possible offers based on who put them and price
    offers = [off for off in response['Items'] if off['username']!=event['username']]
    offers = [(off['id'], float(off['price']), off['username']) for off in offers]
    offers = [off for off in offers if off[1]>=event['price']]
    offers.sort(key=lambda x: x[1])
    
    # No offers, then we create a sell offer
    if len(offers)==0:
        table = dynamodb.Table('Landa_Sell')
        table.put_item(
            Item={
                'id':  str(datetime.datetime.now())+'_'+event['username'],
                'username': event['username'],
                'price': event['price']
            } 
        )
        toreturn = 'Created sell offer for', event['username'], 'at', event['price']

    # We execute the offer and update users
    else:
        # Delete buy offer
        offer = offers[0]
        table = dynamodb.Table('Landa_Buy')
        res = table.delete_item(
            Key={
                'id':  offer[0],
                'username': offer[2]
            } 
        )
        print("Deleted buy offer", offer[0], 'by', offer[2])
        
        # Increment and decrement stock counts
        table = dynamodb.Table('Landa_UserStockCounts')
        response = table.update_item(
            Key={
                'username': event['username']
            },
            UpdateExpression="SET num_stocks = num_stocks - :val",
            ExpressionAttributeValues={
                ':val': decimal.Decimal(1)
            },
            ReturnValues="UPDATED_NEW"
        )
        print("Decremented stock count for", event['username'])
        
        table = dynamodb.Table('Landa_UserStockCounts')
        response = table.update_item(
            Key={
                'username': offer[2]
            },
            UpdateExpression="SET num_stocks = num_stocks + :val",
            ExpressionAttributeValues={
                ':val': decimal.Decimal(1)
            },
            ReturnValues="UPDATED_NEW"
        )
        print("Incremented stock count for", offer[1])
        toreturn = "Executed trade between", offer[1], 'and', event['username']

        # SEND ALERT
    
    return {
        'statusCode': 200,
        'body': toreturn
    }
