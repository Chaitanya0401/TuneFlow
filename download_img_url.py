import boto3
from botocore.exceptions import ClientError
import requests
import os
import json

def download_and_upload_images(bucket_name, json_file):
    # Initialize an S3 client without specifying the region (default region from configuration will be used)
    s3 = boto3.client('s3')

    # Parse the JSON file to get image URLs
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    songs = data.get('songs', [])
    
    for song in songs:
        image_url = song.get('img_url')
        if image_url:
            try:
                # Download the image
                print(f"Downloading image from {image_url}")
                response = requests.get(image_url)
                response.raise_for_status()  # Raise an error if the download failed
                image_data = response.content

                # Extract the image file name from the URL (e.g., 'artist_name.jpg')
                image_name = os.path.basename(image_url)

                # Upload the image to the S3 bucket
                s3.put_object(Bucket=bucket_name, Key=image_name, Body=image_data)
                print(f"Uploaded {image_name} to bucket {bucket_name}.")
            
            except requests.exceptions.RequestException as e:
                print(f"Error downloading {image_url}: {e}")
            except ClientError as e:
                print(f"Error uploading {image_name} to S3: {e}")

# Example Usage
bucket_name = 's4016331-ass1'  # Replace with your bucket name
json_file = '2025a1.json'  # Replace with the path to your JSON file containing song image URLs

# Download and upload the images to the S3 bucket
download_and_upload_images(bucket_name, json_file)
