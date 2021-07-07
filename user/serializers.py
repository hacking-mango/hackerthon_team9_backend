from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from . import models


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = models.User.objects.create(
            email=validated_data["email"],
            password=validated_data["password"],
            nickname=validated_data["nickname"],
            age=validated_data["age"],
            phone=validated_data["phone"],
            position=validated_data["position"],
            profile_image=validated_data["profile_image"],
        )
        password = make_password(validated_data["password"])
        user.password = password
        user.save()
        return user

    class Meta:
        model = models.User
        fields = ["email", "password", "nickname", "age", "phone", "position", "profile_image"]


class FileSerializer(serializers.Serializer):
    profile_image = serializers.ImageField(use_url=True)

    class Meta:
        model = models.User
        fields = ["nickname", "profile_image"]

    # def update(self, validated_data):
    # extension_name = validated_data["file"].name.split(".").pop()  # 입력받은 파일 이름에서 확장자
    # user = "user object"  # 토큰 기준으로 확인한 사용자 객체

    # user.profile_image.save(user.nickname + extension_name, validated_data["file"])  # 입력받은 파일 저장

    # return user


class UserInfoSerializer(serializers.Serializer):
    email = serializers.EmailField()
    age = serializers.IntegerField()
    phone = serializers.CharField()

    class Meta:
        model = models.User
        fields = ["email", "age", "phone"]


class UserUpdateSerializer(serializers.Serializer):
    def update(self, validated_data):

        user = "user object"  # 토큰 기준으로 확인한 사용자 객체

        user.email = validated_data['email']
        user.age = validated_data['age']
        user.phone = validated_data['phone']
        password = make_password(validated_data["password"])
        user.password = password
        user.save()
        return user

    class Meta:
        model = models.User
        fields = ["email", "password", "age", "phone"]
