from django.db import models

from base.common.models import BaseModel


class User(BaseModel):
    email = models.EmailField(max_length=80, unique=True, verbose_name="이메일")
    password = models.TextField(max_length=120, verbose_name="비밀번호")

    class Meta:
        db_table = "user"
        verbose_name = "유저"
        app_label = "user"
