import boto3

# Initialize the DynamoDB client
dynamodb = boto3.client("dynamodb", region_name="us-east-1")  # Change region if needed

# Create the Subscriptions table
try:
    response = dynamodb.create_table(
        TableName="Subscriptions",
        KeySchema=[
            {"AttributeName": "email", "KeyType": "HASH"},  # Partition key
            {"AttributeName": "title", "KeyType": "RANGE"}  # Sort key
        ],
        AttributeDefinitions=[
            {"AttributeName": "email", "AttributeType": "S"},
            {"AttributeName": "title", "AttributeType": "S"}
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        }
    )

    print("✅ Subscriptions table is being created...")
    print("Table status:", response["TableDescription"]["TableStatus"])

except dynamodb.exceptions.ResourceInUseException:
    print("⚠️ Table 'Subscriptions' already exists.")
