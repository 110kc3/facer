from dotenv import load_dotenv
import os
import boto3
import uuid

load_dotenv()
aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
bucket_name = os.environ.get("AWS_S3_BUCKET_NAME")

boto3_aws_client = boto3.client("cognito-idp", region_name="eu-central-1", aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key)

boto3_s3_bucket = boto3.client("s3", region_name="eu-central-1", aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret_access_key)


def upload_file(file):
    """
    Function to upload a file to an S3 bucket
    """
    try:
        new_uuid = str(uuid.uuid4()) + ".png"
        boto3_s3_bucket.upload_fileobj(file, bucket_name, new_uuid, ExtraArgs = {"ContentType": "image/png"})

        return new_uuid
    except:
        raise ValueError(
            '{"code": 400, "message": "Could not add an image to s3 bucket"}')



def download_file(file_name):
    """
    Function to download a given file from an S3 bucket
    """
    s3 = boto3.resource('s3')
    output = f"downloads/{file_name}"
    s3.Bucket(bucket_name).download_file(file_name, output)

    return output


def list_files():
    """
    Function to list files in a given S3 bucket
    """
    
    contents = []
    for item in boto3_s3_bucket.list_objects(Bucket=bucket_name)['Contents']:
        contents.append(item)

    return contents
