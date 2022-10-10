import boto3
from django.conf import settings

s3 = boto3.client("s3")
s3.put_bucket_cors(
    Bucket=settings.AWS_STORAGE_BUCKET_NAME,
    CORSConfiguration=settings.CORS_CONFIGURATION,
)
