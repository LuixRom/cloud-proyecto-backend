import boto3
from datetime import datetime

def lambda_handler(event, context):
    token = event['token']

    dynamodb = boto3.resource('dynamodb')
    t_tokens = dynamodb.Table('t_tokens_acceso')

    response = t_tokens.get_item(Key={
        'token': token
    })

    if 'Item' not in response:
        return {
            'statusCode': 403,
            'body': 'Token no existe'
        }

    expires = response['Item']['expires']
    now = datetime.now().strSftime('%Y-%m-%d %H:%M:%S')

    if now > expires:
        return {
            'statusCode': 403,
            'body': 'Token expirado'
        }

    return {
        'statusCode': 200,
        'body': {
            'message': 'Token válido',
            'tenant_id': response['Item']['tenant_id'],
            'user_id': response['Item']['user_id'],
            'expires': expires
        }
    }
