import os
from datetime import datetime, timedelta

import jwt
from django.contrib.auth.hashers import check_password
from rest_framework import exceptions as exc
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import models, serializers


@api_view(["POST"])
def signup_view(request):
    if request.method == "POST":
        serializer = serializers.SignupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({"success": 1, "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors.keys())
            raise exc.ParseError(code="SIGN-UP-ERROR", detail="회원가입 오류 발생")


@api_view(["POST"])
def login_view(request):
    if request.method == "POST":
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        if any(element is None for element in [email, password]):
            raise exc.ParseError(code="PARAMETER_ERROR", detail="필수 파라미터값이 없습니다.")

        try:
            user = models.User.objects.get(email=email)
        except:  # noqa
            raise exc.NotAuthenticated(code="NOT_FOUND_USER", detail="존재하지 않는 유저 입니다.")

        if not check_password(password, user.password):
            raise exc.NotAuthenticated("패스워드가 일치하지 않습니다.")

        payload = {
            "email": user.email,
            "exp": datetime.now() + timedelta(seconds=60 * 60 * 24),
        }

        jwt_encode = jwt.encode(payload=payload, key=os.environ["SECRET_KEY"], algorithm="HS256")
        token = jwt_encode.decode("utf-8")

        return Response(
            {
                "success": 1,
                "data": {
                    "token": token,
                    "expire_time": datetime.now() + timedelta(seconds=60 * 60 * 24),
                    "email": user.email,
                    "nickname": user.nickname,
                    "profile_image": user.profile_image.url,
                },
            },
            status=status.HTTP_200_OK,
        )


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def user_info_view(request):
    serializer = serializers.UserInfoSerializer(request.user)

    return Response({"success": 1, "data": serializer.data}, status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes((IsAuthenticated,))
def user_update_view(request):
    serializer = serializers.UserUpdateSerializer(instance=request.user, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"success": 1}, status=status.HTTP_200_OK)
    else:
        print(serializer.errors.keys())
        raise exc.ParseError(code="USER-UPDATE-ERROR", detail="사용자 정보 수정 중 오류 발생")


@api_view(["PUT"])
def profile_update_view(request):

    data = request.data
    position_only = not data.pop("flag")

    def process(user, data, serializer, code, detail):

        serializer = serializer(instance=user, data=data)

        if serializer.is_valid():
            serializer.save()

            return Response({"success": 1}, status=status.HTTP_200_OK)
        else:
            print(serializer.errors.keys())
            raise exc.ParseError(code=code, detail=detail)

    config = (
        [serializers.PositionUpdateSerializer, "POSITION-UPDATE-ERROR", "프로필 정보 수정 중 오류 발생"]
        if position_only
        else [serializers.ProfileUpdateSerializer, "PROFILE-UPDATE-ERROR", "프로필 정보 수정 중 오류 발생"]
    )

    return process(request.user, data, *config)
