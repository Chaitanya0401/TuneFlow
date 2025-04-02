import boto3
import json
import time

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb', region_name='us-east-1')

# Create the music table
def create_music_table():
    try:
        response = dynamodb.create_table(
            TableName='music',
            KeySchema=[
                {
                    'AttributeName': 'title',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'year',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'title',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'year',
                    'AttributeType': 'N'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print("Table creation in progress:", response)

        # Wait for the table to be created
        waiter = dynamodb.get_waiter('table_exists')
        waiter.wait(TableName='music')
        print("Table is now ACTIVE!")

    except dynamodb.exceptions.ResourceInUseException:
        print("Table already exists.")

# Load data from JSON file
def load_data_to_table():
    try:
        # Open the JSON file
        with open("2025a1.json") as json_file:
            data = json.load(json_file)

        # Insert data into DynamoDB
        for song in data["songs"]:
            response = dynamodb.put_item(
                TableName='music',
                Item={
                    'title': {'S': song['title']},
                    'year': {'N': song['year']},  # Ensure that year is an integer in DynamoDB
                    'artist': {'S': song['artist']},
                    'album': {'S': song['album']},
                    'img_url': {'S': song['img_url']}
                }
            )
            print(f"Inserted {song['title']} into table.")
    except FileNotFoundError:
        print("File 2025a1.json not found.")
    except Exception as e:
        print(f"Error loading data: {e}")

# Create table and load data
create_music_table()
load_data_to_table()
