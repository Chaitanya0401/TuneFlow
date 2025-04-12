import boto3

dynamodb = boto3.client("dynamodb", region_name="us-east-1")

try:
    response = dynamodb.create_table(
        TableName="Subscriptions",
        KeySchema=[
            {"AttributeName": "email", "KeyType": "HASH"},           # Partition key
            {"AttributeName": "subscription_id", "KeyType": "RANGE"}  # Sort key
        ],
        AttributeDefinitions=[
            {"AttributeName": "email", "AttributeType": "S"},
            {"AttributeName": "subscription_id", "AttributeType": "S"}
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