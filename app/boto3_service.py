import os
import boto3
from dotenv import load_dotenv

load_dotenv()
aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

boto3_client = boto3.client("cognito-idp", region_name="eu-central-1", aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
