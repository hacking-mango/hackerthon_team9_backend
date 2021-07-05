from django.contrib.auth import get_user_model
from rest_framework import serializers
from . import models
from django.contrib.auth.hashers import make_password


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = models.User.objects.create(
            email=validated_data['email'],
            password=validated_data['password'],
        )
        password = make_password(validated_data['password'])
        user.password = password
        user.save()
        return user

    class Meta:
        model = models.User
        fields = ['email', 'password']
