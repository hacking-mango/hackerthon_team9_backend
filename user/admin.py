from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("nickname", "email", "profile_image", "created_at", "position")

    list_display_links = (
        "nickname",
        "email",
    )
