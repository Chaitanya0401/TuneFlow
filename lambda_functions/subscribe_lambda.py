import json
import boto3
import uuid
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
subscriptions_table = dynamodb.Table('Subscriptions')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])

        email = body['email']
        title = body['title']
        artist = body['artist']
        album = body['album']
        year = int(body['year'])
        img_url = body['img_url']
        image_filename = img_url.split("/")[-1]
        s3_url = f"https://s4016331-ass1.s3.amazonaws.com/{image_filename}"

        # Check if already subscribed
        existing = subscriptions_table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("email").eq(email),
            FilterExpression=boto3.dynamodb.conditions.Attr("title").eq(title) & boto3.dynamodb.conditions.Attr("artist").eq(artist)
        )

        if existing.get("Items"):
            return {
                "statusCode": 200,
                "body": json.dumps({"status": "already_subscribed"})
            }

        subscriptions_table.put_item(Item={
            "subscription_id": str(uuid.uuid4()),
            "email": email,
            "title": title,
            "artist": artist,
            "album": album,
            "year": year,
            "image_url": s3_url
        })

        return {
            "statusCode": 200,
            "body": json.dumps({"status": "success"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }