from rest_framework import exceptions as exc

from base.common import utill


# 로그인확인 데코레이터
class LoginCheck:
    def __init__(self, ori_function):
        self.redis = utill.REDIS()
        self.ori_function = ori_function

    def __call__(self, request, *args, **kwargs):
        token = request.headers.get("token", None)
        check_token = self.redis.session_check(token)
        if check_token["success"] != 1:
            raise exc.ParseError(code=check_token["errorCode"], detail=check_token["errorMessage"])
        return self.ori_function(self, request, *args, **kwargs)
