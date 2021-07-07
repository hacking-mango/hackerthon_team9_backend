import os

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_S3_REGION_NAME = "ap-northeast-2"

AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"

# 이후에 필요한 경우, 아래 항목에서 파라미터 설정
# AWS_S3_OBJECT_PARAMETERS = {
# 'CacheControl': 'max-age=86400',
# }

AWS_S3_SECURE_URLS = False # https 사용 여부
AWS_QUERYSTRING_AUTH = False # 인증 관련 쿼리 파라미터 허용 여부

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# referenced web page1 : https://richone.tistory.com/7
# referenced web page2 : https://ssungkang.tistory.com/entry/Django-AWS-S3를-이용한-이미지-업로드
