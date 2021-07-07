from rest_framework import exceptions as exc
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import serializers


@api_view(["GET", "POST"])
def user_view(request):
    if request.method == "GET":
        email = request.GET.get("email")
        password = request.Get.get("password")

        if not email:
            raise exc.ParseError("이메일 파라미터가 없습니다.")

        if not password:
            raise exc.ParseError("비밀번호 파라미터가 없습니다.")

        # jwt 인증관련 로그인 구현
        pass
    if request.method == "POST":
        serializer = serializers.SignupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({"success": 1, "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors.keys())
            raise exc.ParseError(code="SIGN-UP-ERROR", detail="회원가입 오류 발생")

@api_view(["PUT"])
def profile_update_view(request):

    data = request.data
    position_only = not data.pop('flag')

    if position_only:
        serializer = serializers.PositionUpdateSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response({"success": 1}, status=status.HTTP_200_OK)
        else:
            print(serializer.errors.keys())
            raise exc.ParseError(code="POSITION-UPDATE-ERROR", detail="포지션 정보 수정 중 오류 발생")

    serializer = serializers.ProfileUpdateSerializer(data=data)

    if serializer.is_valid():
        serializer.save()

        return Response({"success": 1}, status=status.HTTP_200_OK)
    else:
        print(serializer.errors.keys())
        raise exc.ParseError(code="PROFILE-UPDATE-ERROR", detail="프로필 정보 수정 중 오류 발생")
