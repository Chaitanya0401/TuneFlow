import boto3
import json
import requests
import os
from botocore.exceptions import ClientError

# Configuration settings
bucket_name = 's4016331-ass1'  # Replace with your actual S3 bucket name
region = 'us-east-1'
s3 = boto3.client('s3', region_name=region)

def create_bucket():
    try:
        if region == 'us-east-1':
            # For us-east-1, do not specify CreateBucketConfiguration
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        print(f"S3 bucket '{bucket_name}' created successfully.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            print(f"S3 bucket '{bucket_name}' already exists and is owned by you.")
        else:
            raise

# Download artist images from URLs and upload them to S3
def download_and_upload_images():
    with open('data/2025a1.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    os.makedirs('images', exist_ok=True)

    image_urls = set(song['img_url'] for song in data['songs'])
    print(f"Downloading {len(image_urls)} unique artist images...\n")

    for url in image_urls:
        file_name = url.split('/')[-1]
        file_path = f'images/{file_name}'

        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Save image locally
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded image: {file_name}")

                # Upload image to S3 with public access
                s3.upload_file(
                    file_path,
                    bucket_name,
                    file_name,
                    ExtraArgs={'ACL': 'public-read'}
                )
                print(f"Uploaded to S3: {file_name}")
            else:
                print(f"Failed to download {file_name} - HTTP status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred while processing {file_name}: {e}")

    print("\nAll images have been downloaded and uploaded to S3.")

# Update image URLs in the JSON file to point to the S3 bucket
def update_image_urls():
    s3_base_url = f"https://{bucket_name}.s3.{region}.amazonaws.com"

    with open('2025a1.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for song in data['songs']:
        file_name = song['img_url'].split('/')[-1]
        song['img_url'] = f"{s3_base_url}/{file_name}"

    with open('updated_2025a1.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    print("Updated image URLs saved to 'updated_2025a1.json'.")

# Main execution
if __name__ == '__main__':
    create_bucket()
    download_and_upload_images()
    update_image_urls()
