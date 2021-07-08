from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", include("user.urls"), name="user"),
    path("chat/", include("chat.urls"), name="chat"),
]
