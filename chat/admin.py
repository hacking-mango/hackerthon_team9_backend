from django.contrib import admin

from .models import Room, Message, Match


@admin.register(Room)
class Room(admin.ModelAdmin):
    list_display = ('room_hash', 'activate', 'room_name')

    list_display_links = (
        "room_hash",
        "activate",
        "room_name",
    )
