import boto3
from botocore.exceptions import ClientError

def create_s3_bucket(bucket_name, region='us-east-1'):
    # Initialize an S3 client
    s3 = boto3.client('s3', region_name=region)

    try:
        # Check if the bucket exists
        response = s3.list_buckets()
        bucket_exists = any(bucket['Name'] == bucket_name for bucket in response['Buckets'])
        
        if not bucket_exists:
            # For 'us-east-1', no need to add LocationConstraint
            if region == 'us-east-1':
                s3.create_bucket(Bucket=bucket_name)
            else:
                s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': region}
                )
            print(f"Bucket '{bucket_name}' created successfully in region '{region}'.")
        
        # Verify the bucket creation by getting its location
        bucket_location = s3.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
        print(f"Bucket location: {bucket_location if bucket_location else 'us-east-1 (default)'}")

    except ClientError as e:
        print(f"Error: {e}")

# Replace these with your desired bucket name
bucket_name = 's4016331-ass1'  # Replace with your own unique bucket name

# Create the bucket in the default region (us-east-1)
create_s3_bucket(bucket_name)
