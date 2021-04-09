import boto3
from gensim.models import Word2Vec

s3_client = boto3.client('s3')
lex_client = boto3.client('lex-runtime')

async def hobbyHandler(event, context):
    userId = event['userId']
    intentName = event['currentIntent']['name']

    print('Request received for userId={}, intentName={}'.format(userId, intentName))
    sessionAttributes = event['sessionAttributes']
    slots = event['currentIntent']['slots']

    name = slots['Name']
    hobby = slots['Hobby']

    messageString = {'contentType': 'PlainText', 'content': 'Okay, your name is {} and your hobby is {}.'.format(name, hobby)}
    fulfillmentState = 'Fulfilled'

    response = lex_client.put_session(
        sessionAttributes,
        dialogAction = {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled',
            'message': messageString
        }
    )

    return response
