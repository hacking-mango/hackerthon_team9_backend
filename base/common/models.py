from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="생성일")
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="수정일")
    deleted_yn = models.CharField(max_length=1, default=0, blank=True, null=True, verbose_name="삭제여부")

    class Meta:
        abstract = True
