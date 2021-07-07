from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.user_view, name="sign-up"),
    path("login/", views.user_view, name="login"),
    path("info/", views.user_info_view, name="info"),
    path("update/info/", views.user_view, name="user-update"),
]
