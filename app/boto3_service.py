from dotenv import load_dotenv
import os
import boto3
import uuid


from PIL import Image
from io import BytesIO
import numpy as np
import base64

load_dotenv()
aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
bucket_name = os.environ.get("AWS_S3_BUCKET_NAME")

boto3_aws_client = boto3.client("cognito-idp", region_name="eu-central-1", aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key)

boto3_s3_bucket = boto3.client("s3", region_name="eu-central-1", aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret_access_key)

    
boto3_s3_bucket_resource = boto3.resource("s3", region_name="eu-central-1", aws_access_key_id=aws_access_key_id,
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



def read_image_from_s3(key):
    """Load image file from s3.

    Parameters
    ----------
    bucket: string
        Bucket name
    key : string
        Path in s3

    Returns
    -------
    np array
        Image array
    """
    s3 = boto3_s3_bucket_resource
    bucket = s3.Bucket(bucket_name)
    object = bucket.Object(key)
    response = object.get()
    file_stream = response['Body']
    image = Image.open(file_stream)
    #Converting PIL Image.image object to base64 string
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
 
    return img_str



def list_files():
    """
    Function to list files in a given S3 bucket
    """
    
    contents = []
    for item in boto3_s3_bucket.list_objects(Bucket=bucket_name)['Contents']:
        contents.append(item)

    return contents
