import json
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
login_table = dynamodb.Table('login')

def lambda_handler(event, context):
    try:
        # Ensure 'body' is in event
        if 'body' not in event:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing body in request'})
            }

        data = json.loads(event['body'])  # Parse JSON string body
        email = data['email']
        username = data['username']
        password = data['password']

        # Check if user already exists
        existing = login_table.get_item(Key={'email': email})
        if 'Item' in existing:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Email already exists'})
            }

        # Add user
        login_table.put_item(Item={
            'email': email,
            'user_name': username,
            'password': password
        })

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User registered successfully'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }