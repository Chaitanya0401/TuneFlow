import boto3
import json

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb', region_name='us-east-1')

def create_login_table():
    try:
        response = dynamodb.create_table(
            TableName='login',
            KeySchema=[
                {
                    'AttributeName': 'email',
                    'KeyType': 'HASH'  # Primary Key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'email',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print("Table creation in progress:", response)
        
        # Wait for table creation
        waiter = dynamodb.get_waiter('table_exists')
        waiter.wait(TableName='login')
        print("Table is now ACTIVE!")
    
    except dynamodb.exceptions.ResourceInUseException:
        print("Table already exists.")

def load_data_to_table():
    try:
        with open("users.json") as json_file:
            data = json.load(json_file)

        for user in data["users"]:
            response = dynamodb.put_item(
                TableName='login',
                Item={
                    'email': {'S': user['email']},
                    'user_name': {'S': user['user_name']},
                    'password': {'S': user['password']}
                }
            )
            print(f"Inserted {user['email']} into table.")
    except FileNotFoundError:
        print("File users.json not found.")
    except Exception as e:
        print(f"Error loading data: {e}")

# Call functions to create the table and load data
create_login_table()
load_data_to_table()
