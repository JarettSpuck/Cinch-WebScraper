import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize a session using environment variables
session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION', 'us-east-1')  # Default to us-east-1 if not specified
)

s3 = session.client('s3')
BUCKET_NAME = os.getenv('BUCKET_NAME')

def upload_to_s3(file_path, file_name):
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"Error: The file {file_path} does not exist.")
        return

    try:
        s3.upload_file(file_path, BUCKET_NAME, file_name)
        print(f"Successfully uploaded {file_name} to {BUCKET_NAME}")
    except Exception as e:
        print(f"Failed to upload {file_name} to {BUCKET_NAME}: {e}")

# Example usage
upload_to_s3('path/to/your/file.txt', 'file.txt')
