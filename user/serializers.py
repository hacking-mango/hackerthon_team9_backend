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
