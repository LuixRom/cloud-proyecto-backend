import json
import requests
import os

def lambda_handler(event, context):
    for record in event['Records']:
        if record['eventName'] == 'INSERT':
            new_image = record['dynamodb']['NewImage']
            producto = {
                "producto_id": new_image['producto_id']['S'],
                "nombre": new_image['nombre']['S'],
                "precio": float(new_image['precio']['N']),
                "descripcion": new_image.get('descripcion', {}).get('S', ''),
                "tenant_id": new_image['tenant_id']['S']
            }
            tenant_id = producto["tenant_id"]
            port = f"920{tenant_id[-1]}" 
            url = f"http://<IP_VM>:{port}/productos/_doc/{producto['producto_id']}"
            requests.put(url, json=producto)
    return {"statusCode": 200}
q