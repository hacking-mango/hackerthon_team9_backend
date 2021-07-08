import os
import jwt
from django.apps import apps
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions


class Token(BaseAuthentication):
    def authenticate(self, request):

        access_token = request.META.get("HTTP_TOKEN", None) # header: {'TOKEN' or 'token': token}

        if not access_token or access_token == "undefined":
            return None
        try:
            decoded = jwt.decode(access_token, key=os.environ["SECRET_KEY"], algorithm="HS256")
        except Exception as ex:
            print(ex)
            return None

        user = apps.get_model("user", "User")
        user_key = decoded.get("email")

        try:
            user = user.objects.get(email=user_key)

            user.is_authenticated = True

            return (user, True)
            # (user, auth) => (사용자, 인증 여부)
            # https://www.django-rest-framework.org/api-guide/authentication/#custom-authentication

        except user.DoesNotExist:
            raise exceptions.AuthenticationFailed({"success": 0, "results": "authentication failed"})
