from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.views import status


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
