import json
import requests
import os

def lambda_handler(event, context):
    for record in event['Records']:
        if record['eventName'] == 'INSERT':
            new_image = record['dynamodb']['NewImage']
            compra = {
                "compra_id": new_image['compra_id']['S'],
                "user_id": new_image['user_id']['S'],
                "productos": [json.loads(item['S']) for item in new_image['productos']['L']],
                "total": float(new_image['total']['N']),
                "fecha": new_image.get('fecha', {}).get('S', ''),
                "tenant_id": new_image['tenant_id']['S']
            }
            tenant_id = compra["tenant_id"]
            port = f"920{tenant_id[-1]}"
            url = f"http://<IP_VM>:{port}/compras/_doc/{compra['compra_id']}"
            requests.put(url, json=compra)
    return {"statusCode": 200}
