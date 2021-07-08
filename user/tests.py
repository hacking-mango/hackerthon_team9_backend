import os
from datetime import datetime, timedelta

import jwt
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.views import status

from . import models


class SignUpTest(APITestCase):
    def test_signup_success(self):

        params = {
            "email": "tjdntjr123@gmail.com",
            "nickname": "hello",
            "password": "qwer1234",
            "age": 28,
            "phone": "010-4242-2048",
            "position": "backend",
            "profile_image": SimpleUploadedFile("test.jpg", b"whatevercontentsyouwant"),
        }

        url = reverse("sign-up")

        self.assertEqual(url, "/user/signup/")
        res = self.client.post(url, data=params, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


class UserInfoTest(APITestCase): # 잘못된 토큰을 전달받은 상황은 나중에
    def setUp(self):
        test_user = models.User.objects.create(
            email="email@for.test",
            password="test_password",
            nickname="test_user",
            age=20,
            phone="010-0000-0000",
            position="backend",
            profile_image=SimpleUploadedFile("test.jpg", b"test_content"),
        )

        payload = {
            "email": test_user.email,
            "exp": datetime.now() + timedelta(seconds=60 * 60 * 24),
        }

        jwt_encode = jwt.encode(payload=payload, key=os.environ["SECRET_KEY"], algorithm="HS256")
        token = jwt_encode.decode("utf-8")

        self.user = test_user
        self.token = token

    def test_user_info_success(self): # 요청에 성공한 상황
        success_data = {
            "success": 1,
            "data": {
                "email": self.user.email,
                "age": self.user.age,
                "phone": self.user.phone,
            },
        }
        url = reverse("info")
        header = {'HTTP_TOKEN': self.token}

        self.assertEqual(url, "/user/info/")
        res = self.client.get(url, **header)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, success_data)

    def test_user_info_without_token(self): # 토큰이 없는 상황
        failure_data = {
            "success": 0,
            "data": {
                "code": "not_authenticated",
                "message": "Authentication credentials were not provided."
            }
        }
        url = reverse("info")
        header = {'HTTP_TOKEN': None}

        self.assertEqual(url, "/user/info/")
        res = self.client.get(url, **header)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data, failure_data)
