import os

from .common import BASE_DIR

AWS_ACCESS_KEY_ID = "Access key ID"
AWS_SECRET_ACCESS_KEY = "Secret access Key"

AWS_S3_REGION_NAME = "REGION_NAME"

###S3 Storages
AWS_STORAGE_BUCKET_NAME = "STORAGE-NAME"
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"

# 이후에 필요한 경우, 아래 항목에서 파라미터 설정
# AWS_S3_OBJECT_PARAMETERS = {
# 'CacheControl': 'max-age=86400',
# }

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
MEDIA_ROOT = os.path.join(BASE_DIR, "path/to/store/my/files/")

# referenced web page : https://richone.tistory.com/7
