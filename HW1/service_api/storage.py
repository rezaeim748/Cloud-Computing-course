import os, boto3
from botocore.client import Config

S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_REGION = os.getenv("S3_REGION", "us-east-1")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_PRESIGN_EXPIRY = int(os.getenv("S3_PRESIGN_EXPIRY", "3600"))

s3 = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT_URL,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
    region_name=S3_REGION,
    config=Config(signature_version="s3v4"),
    verify=False,
)

def put_image(key: str, data: bytes, content_type: str):
    s3.put_object(Bucket=S3_BUCKET, Key=key, Body=data, ContentType=content_type)

def presign_get(key: str, expires=S3_PRESIGN_EXPIRY):
    return s3.generate_presigned_url("get_object", Params={"Bucket": S3_BUCKET, "Key": key}, ExpiresIn=expires)
