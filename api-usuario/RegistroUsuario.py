import boto3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def lambda_handler(event, context):
    tenant_id = event['tenant_id']
    user_id = event['user_id']
    password = event['password']

    dynamodb = boto3.resource('dynamodb')
    t_usuarios = dynamodb.Table('t_usuarios')

    response = t_usuarios.get_item(Key={
        'tenant_id': tenant_id,
        'user_id': user_id
    })

    if 'Item' in response:
        return {
            'statusCode': 409,
            'body': {
                'error': 'El usuario ya existe en este tenant'
            }
        }
S
    hashed_password = hash_password(password)

    t_usuarios.put_item(
        Item={
            'tenant_id': tenant_id,
            'user_id': user_id,
            'password': hashed_password
        }
    )

    return {
        'statusCode': 201,
        'body': {
            'message': 'Usuario registrado exitosamente',
            'tenant_id': tenant_id,
            'user_id': user_id
        }
    }
