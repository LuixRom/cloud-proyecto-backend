import boto3
import json
import uuid
from datetime import datetime

def lambda_handler(event, context):
    print(event)
    body = json.loads(event['body'])
    token = event['headers']['Authorization']


    lambda_client = boto3.client('lambda')
    payload = json.dumps({ "token": token })
    response = lambda_client.invoke(
        FunctionName="ValidarTokenAcceso",
        InvocationType='RequestResponse',
        Payload=payload
    )
    validation = json.loads(response['Payload'].read())
    if validation['statusCode'] == 403:
        return {
            'statusCode': 403,
            'body': 'Token inválido'
        }


    tenant_id = body['tenant_id']
    user_id = body['user_id']
    productos = body['productos']  
    total = body.get('total', 0)

    compra = {
        'tenant_id': tenant_id,
        'compra_id': str(uuid.uuid4()),
        'user_id': user_id,
        'productos': productos,
        'total': total,
        'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_compras')
    table.put_item(Item=compra)

    return {
        'statusCode': 201,
        'body': json.dumps({ 'message': 'Compra registrada', 'compra': compra })
    }
