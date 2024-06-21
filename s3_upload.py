import boto3
import os
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client('s3')
BUCKET_NAME = os.getenv('BUCKET_NAME')

def upload_to_s3(file_path, file_name):
    try:
        s3.upload_file(file_path, BUCKET_NAME, file_name)
        print(f"Successfully uploaded {file_name} to {BUCKET_NAME}")
    except Exception as e:
        print(f"Failed to upload {file_name} to {BUCKET_NAME}: {e}")
