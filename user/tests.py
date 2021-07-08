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


class UserInfoTest(APITestCase):
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
