import boto3
import os
s3 = boto3.client("s3")
bucket_name = os.environ.get("S3_BUCKET")
def download_video(key)->str:
    file_path = "/tmp/videos/"+key
    print("downloadedr", file_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    s3.download_file(
        bucket_name,
        key,
        file_path
    )
    return file_path
def download_img(key)->str:
    file_path = "/tmp/images/"+key
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    s3.download_file(
        bucket_name,
        key,
        file_path
    )
    return file_path
def upload_video(key,file)->str:
    s3.upload_file(
        file,
        bucket_name,
        key
    )
    return key
def download_image(key)->str:
    return download_img(key)
def upload_image(key,file)->str:
    s3.upload_file(
        file,
        bucket_name,
        key
    )
    return key
    