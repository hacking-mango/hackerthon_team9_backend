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

        return Response(
            {"success": 0, "error_code": "SIGN-UP-ERROR", "message": "회원가입을 하는 도중 오류가 발생했습니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )
