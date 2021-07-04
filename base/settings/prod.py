from .common import *

DEBUG = os.environ.get("DEBUG") in ["1", "t", "true", "T", "True"]

CORS_ORIGIN_WHITELIST = os.environ.get("CORS_ORIGIN_WHITELIST", "").split(",")

CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ORIGIN_WHITELIST", "").split(",")


