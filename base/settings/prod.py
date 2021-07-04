from .common import *  # noqa

DEBUG = os.environ.get("DEBUG") in ["1", "t", "true", "T", "True"]  # noqa

CORS_ORIGIN_WHITELIST = os.environ.get("CORS_ORIGIN_WHITELIST", "").split(",")  # noqa

CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ORIGIN_WHITELIST", "").split(",")  # noqa
