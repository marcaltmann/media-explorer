"""S3 wrappers"""

from urllib.parse import urljoin
from explorer.config import Settings

settings = Settings.from_env()


def store_file(file: str, filename: str) -> str:
    """Takes a file path, returns object store url."""
    s3_client = settings.s3.get_client()
    s3_client.upload_file(file, settings.s3.S3_BUCKET_NAME, filename)
    return f'{settings.s3.get_bucket_url()}/{filename}'


def store_fileobj(fileobj: any, filename: str) -> str:
    """Take a fileobj(?), returns object store url."""
    s3_client = settings.s3.get_client()
    s3_client.upload_fileobj(fileobj, settings.s3.S3_BUCKET_NAME, filename)
    return f'{settings.s3.get_bucket_url()}/{filename}'
