from django.contrib.auth.models import BaseUserManager
from django.db import models

from base.common.models import BaseModel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_superuser(self, email, nickname, password):
        user = self.create_user(email=self.normalize_email(email), nickname=nickname, password=password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(BaseModel):
    objects = UserManager()

    email = models.EmailField(max_length=80, unique=True, verbose_name="이메일")
    nickname = models.CharField(max_length=50, verbose_name="닉네임")
    age = models.IntegerField(blank=True, verbose_name="나이")
    phone = models.CharField(blank=True, max_length=13, verbose_name="핸드폰번호")
    position = models.CharField(blank=True, max_length=10, verbose_name="포지션")
    profile_image = models.ImageField(
        blank=True,
        upload_to="accounts/profile/%Y/%m/%d",
        help_text="48px * 48px 크기의 png/jpg 파일을 업로드해주세요.",
        verbose_name="이미지경로",
    )
    password = models.CharField(max_length=128, verbose_name="비밀번호")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "nickname"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        db_table = "user"
        verbose_name = "유저"
        app_label = "user"
