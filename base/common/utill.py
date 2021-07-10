import redis
from django.conf import settings

REDIS_INFO = settings.REDIS if hasattr(settings, "REDIS") else None


class REDIS:
    # Redis 커넥션 생성
    def __init__(self):
        if REDIS_INFO:
            self.redis_drive = redis.StrictRedis(
                host=REDIS_INFO["host"],
                port=REDIS_INFO["port"],
                password=REDIS_INFO["password"],
                db=REDIS_INFO["db"],
            )
        else:
            self.redis_drive = redis.StrictRedis()

    # 로그인
    def session_set(self, operator_id, jwt_token):
        # 토큰 생성
        # sessionToken = getRandomCertificationNumber()[0]
        sessionToken = jwt_token
        # 세션 저장
        # sessionInfo["keyType"] = "sessionToken"
        self.redis_drive.set(sessionToken, operator_id)
        # 토큰 반환
        return sessionToken

    # 세션 체크
    def session_check(self, jwt_token):
        if jwt_token is None:
            return {
                "success": 0,
                "errorCode": "sessionCheck_001",
                "errorMessage": "sessionToken 값이 없음",
            }
        token_info = self.redis_drive.get(jwt_token)
        if token_info is None:
            return {
                "success": 0,
                "errorCode": "sessionCheck_002",
                "errorMessage": "session 없음.",
            }
        return {"success": 1, "token_info": token_info}

    # 로그아웃
    def session_delete(self, jwt_token):
        token_info = self.redis_drive.get(jwt_token)
        if token_info is None:
            return {"success": 1}
        self.redis_drive.delete(jwt_token)
        return {"success": 1}

    def get_key(self, key):
        return self.redis_drive.get(key)

    def set_key(self, key):
        return self.redis_drive.set(key)
