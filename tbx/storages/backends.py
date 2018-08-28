from storages.backends.s3boto3 import S3Boto3Storage


class S3Boto3StorageWithQuerystring(S3Boto3Storage):
    """
    Serve files from S3 with querystring and short expiry period.

    It's used for generating signed URLs on the document view.
    """
    querystring_auth = True
    querystring_expire = 150
    custom_domain = None
