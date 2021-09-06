# mini_landa

Frontend was created with React JS. On loading a user enters his username and enters. A function is called which checks through the API whether the user already exists and if so fetches its stock count. Otherwise, the lambda connected to the API will create a new use of that name with 0 stocks.
After log-in, the user has the ability to buy and sell shares, each of these is a call to the API.

The API is done using API Gateway, one API handles the user logging in, another a buy offer and the last a sell offer.
Each API is routed to its own lambda function.

The data is stored in three DynamoDBs, one in charge of holding usernames and amount of stocks owned, another of buy offers (id, username, price) and the last for sell offers (id, username, price)

The real-time update of stock owned was to be updated using MQTT, having each user listen to subscribe to data attributed to its username. When trades are executed, the lambdas would then send messegest through the MQTT with the relevant topics (usernames). This was not implemented yet.
