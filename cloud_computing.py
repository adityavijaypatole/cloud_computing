import boto3
import json
import string
import random

dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
table = dynamodb.Table('UrlMapping')

# Helper for CORS headers
CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
}

def lambda_handler(event, context):
    path = event.get('rawPath', '/').strip('/')
    # Fix for method detection in Function URLs
    method = event.get('requestContext', {}).get('http', {}).get('method', 'GET')

    # 0. Handle OPTIONS (Pre-flight request)
    if method == 'OPTIONS':
        return {'statusCode': 204, 'headers': CORS_HEADERS}

    # 1. REDIRECT & TRACK CLICKS (GET)
    if method == 'GET' and path:
        try:
            response = table.update_item(
                Key={'short_id': path},
                UpdateExpression="SET clicks = if_not_exists(clicks, :start) + :inc",
                ExpressionAttributeValues={':inc': 1, ':start': 0},
                ReturnValues="ALL_NEW"
            )
            if 'Attributes' in response:
                return {
                    'statusCode': 302,
                    'headers': {
                        'Location': response['Attributes']['long_url'],
                        **CORS_HEADERS
                    }
                }
        except Exception:
            pass
        return {'statusCode': 404, 'headers': CORS_HEADERS, 'body': 'URL not found'}

    # 2. CREATE SHORT URL (POST)
    if method == 'POST':
        try:
            body = json.loads(event.get('body', '{}'))
            long_url = body.get('long_url')
            if not long_url:
                return {'statusCode': 400, 'headers': CORS_HEADERS, 'body': 'Missing long_url'}
            
            short_id = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            table.put_item(Item={'short_id': short_id, 'long_url': long_url, 'clicks': 0})
            
            url_base = "https://sv4dt5drhfueekdu55cm26vub40sqrti.lambda-url.eu-north-1.on.aws/"
            return {
                'statusCode': 200,
                'headers': CORS_HEADERS,
                'body': json.dumps({'short_url': f"{url_base}{short_id}"})
            }
        except Exception as e:
            return {'statusCode': 500, 'headers': CORS_HEADERS, 'body': str(e)}

    return {'statusCode': 200, 'headers': CORS_HEADERS, 'body': 'API is Live'}
