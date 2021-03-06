from django.conf.urls import url  # noqa
from django.urls import path

from . import views

urlpatterns = [
    # url(r"^$", views.index, name="index"),
    # url(r"^(?P<room_name>[^/]+)/$", views.room, name="room"),
    path("matching/", views.matching_view, name="matching"),
    path("room/create/", views.create_room_view, name="create-room"),
    path("room/update/", views.update_room_view, name="update-room"),
    path("room/", views.get_room_view, name="get-room"),
    path("room/leave", views.leave_room_view, name="leave-room"),
    path("messages/", views.get_messages_view, name="get-messages"),
]
