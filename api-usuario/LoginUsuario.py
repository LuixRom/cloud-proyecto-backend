import boto3
import hashlib
import uuid
from datetime import datetime, timedelta

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def lambda_handler(event, context):
    tenant_id = event['tenant_id']
    user_id = event['user_id']
    password = event['password']

    hashed_password = hash_password(password)
    dynamodb = boto3.resource('dynamodb')
    t_usuarios = dynamodb.Table('t_usuarios')

    response = t_usuarios.get_item(Key={
        'tenant_id': tenant_id,
        'user_id': user_id
    })

    if 'Item' not in response:
        return {
            'statusCode': 403,
            'body': 'Usuario no existe'
        }

    hashed_password_bd = response['Item']['password']
    if hashed_password != hashed_password_bd:
        return {
            'statusCode': 403,
            'body': 'Contraseña incorrecta'
        }

    token = str(uuid.uuid4())
    fecha_hora_exp = datetime.now() + timedelta(hours=1)

    t_tokens = dynamodb.Table('t_tokens_acceso')
    t_tokens.put_item(Item={
        'token': token,
        'expires': fecha_hora_exp.strftime('%Y-%m-%d %H:%M:%S'),
        'tenant_id': tenant_id,
        'user_id': user_id
    })

    return {
        'statusCode': 200,
        'body': {
            'message': 'Login exitoso',
            'token': token,
            'expires': fecha_hora_exp.strftime('%Y-%m-%d %H:%M:%S')
        }
    }
