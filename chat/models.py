from django.db import models

from base.common.models import BaseModel
from user.models import User


class Room(BaseModel):
    room_hash = models.CharField(max_length=80, unique=True, verbose_name="방 해시값")
    activate = models.BooleanField(verbose_name="매칭 기능 활성화 여부")
    room_name = models.CharField(max_length=50, verbose_name="방 이름")
    max_planner = models.IntegerField(verbose_name="기획자 정원")
    max_designer = models.IntegerField(verbose_name="디자이너 정원")
    max_frontend = models.IntegerField(verbose_name="프론트엔드 정원")
    max_backend = models.IntegerField(verbose_name="백엔드 정원")
    max_aosdev = models.IntegerField(verbose_name="AOS 개발자 정원")
    max_iosdev = models.IntegerField(verbose_name="iOS 개발자 정원")

    class Meta:
        db_table = "room"
        verbose_name = "채팅방"
        app_label = "chat"


class Match(BaseModel):
    position = models.CharField(blank=True, max_length=10, verbose_name="포지션")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="사용자")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, verbose_name="채팅방")

    class Meta:
        db_table = "match"
        verbose_name = "매칭풀"
        app_label = "chat"


class Message(BaseModel):
    content = models.TextField(blank=True, verbose_name="채팅 내용")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="사용자")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, verbose_name="채팅방")

    class Meta:
        db_table = "message"
        verbose_name = "메시지"
        app_label = "chat"
