import os
from datetime import datetime, timedelta

import jwt
from django.contrib.auth.hashers import check_password
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.views import status

from . import models

small_gif = (
    b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
    b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
    b"\x02\x4c\x01\x00\x3b"
)


class SignUpTest(APITestCase):
    def tearDown(self):
        models.User.objects.all().delete()

    def test_signup_success(self):

        params = {
            "email": "email@for.test",
            "password": "test_password",
            "nickname": "test_user",
            "age": 20,
            "phone": "010-0000-0000",
            "position": "backend",
            "profile_image": SimpleUploadedFile("small.gif", small_gif, content_type="image/gif"),
        }

        url = reverse("sign-up")

        self.assertEqual(url, "/user/signup/")
        res = self.client.post(url, data=params)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


class TestWithUser(APITestCase):
    NO_TOKEN_RESPONSE = {
        "success": 0,
        "data": {"code": "not_authenticated", "message": "Authentication credentials were not provided."},
    }

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

    def tearDown(self):
        models.User.objects.all().delete()


class UserInfoTest(TestWithUser):  # 잘못된 토큰을 전달받은 상황은 나중에
    URL = reverse("info")
    END_POINT = "/user/info/"

    def test_user_info_success(self):  # 요청에 성공한 상황
        success_data = {
            "success": 1,
            "data": {
                "email": self.user.email,
                "age": self.user.age,
                "phone": self.user.phone,
            },
        }
        header = {"HTTP_TOKEN": self.token}

        self.assertEqual(self.URL, self.END_POINT)
        res = self.client.get(self.URL, **header)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, success_data)

    def test_user_info_without_token(self):  # 토큰이 없는 상황
        header = {"HTTP_TOKEN": None}

        self.assertEqual(self.URL, self.END_POINT)
        res = self.client.get(self.URL, **header)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data, self.NO_TOKEN_RESPONSE)


class UserUpdateTest(TestWithUser):
    URL = reverse("user-update")
    END_POINT = "/user/update/info/"
    PARAMS = {
        "email": "changed_email@for.test",
        "password": "changed_password",
        "age": 30,
        "phone": "010-1111-1111",
    }

    def test_user_update_success(self):  # 요청에 성공한 상황
        success_data = {"success": 1}
        header = {"HTTP_TOKEN": self.token}

        self.assertEqual(self.URL, self.END_POINT)
        res = self.client.put(self.URL, data=self.PARAMS, format="json", **header)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, success_data)

        self.user.refresh_from_db()
        password_match = check_password(self.PARAMS["password"], self.user.password)

        self.assertEqual(self.user.email, self.PARAMS["email"])
        self.assertTrue(password_match)
        self.assertEqual(self.user.age, self.PARAMS["age"])
        self.assertEqual(self.user.phone, self.PARAMS["phone"])

    def test_user_update_without_token(self):  # 토큰이 없는 상황
        header = {"HTTP_TOKEN": None}

        self.assertEqual(self.URL, self.END_POINT)
        res = self.client.put(self.URL, data=self.PARAMS, format="json", **header)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data, self.NO_TOKEN_RESPONSE)

        self.user.refresh_from_db()
        password_match = check_password(self.PARAMS["password"], self.user.password)

        self.assertNotEqual(self.user.email, self.PARAMS["email"])
        self.assertFalse(password_match)
        self.assertNotEqual(self.user.age, self.PARAMS["age"])
        self.assertNotEqual(self.user.phone, self.PARAMS["phone"])
