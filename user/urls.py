from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.signup_view, name="sign-up"),
    path("login/", views.login_view, name="login"),
    path("info/", views.user_info_view, name="info"),
    path("update/info/", views.user_update_view, name="user-update"),
    path("update/profile/", views.profile_update_view, name="profile-update"),
]
