import os
import json


from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')


def translate(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    
    lang = event['pathParameters']['language']
    
    
    client = boto3.client('translate', region_name="us-east-1")
    trans_text=client.translate_text(Text=result['Item']['text'], SourceLanguageCode="auto", TargetLanguageCode=lang)
    
    result['Item']['text']=trans_text['TranslatedText']

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }
    

    return response