import boto3
import json
from boto3.dynamodb.conditions import Key

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

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_compras')

    response = table.query(
        IndexName='idx_usuario',
        KeyConditionExpression=Key('tenant_id').eq(tenant_id) & Key('user_id').eq(user_id)
    )

    return {S
        'statusCode': 200,
        'body': json.dumps({
            'compras': response.get('Items', []),
            'cantidad': response.get('Count', 0)
        })
    }
