import json

from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils.safestring import mark_safe
from rest_framework import exceptions as exc
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user.models import User

from .models import Match, Message, Room
from .serializers import CreateRoomSerializer, UpdateRoomSerializer

POSITIONS = ["planner", "designer", "frontend", "backend", "aosdev", "iosdev"]


def index(request):
    return render(request, "chat/index.html", {})


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name_json": mark_safe(json.dumps(room_name))})


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def matching_view(request):
    user = request.user

    user_match, new_matching = Match.objects.get_or_create(user=user, position=user.position)
    # 대기 중인 사용자, 매칭이 새로 생성된 지 여부

    if not new_matching:
        # 매칭이 새로 생성되지 않음 == 기존에 매칭이 있음
        raise exc.ParseError(code="MATCHING_ALREADY_EXISTS", detail="이미 매칭풀에 존재하는 사용자")

    user = request.user
    valid_room = Room.objects.filter(deleted_yn=0)  # deleted_yn = 매칭 완료 여부

    if valid_room:
        # 매칭 완료가 되지 않은 방이 있다면
        return room_matching(user, user_match, valid_room)

    return random_matching(user)


def room_matching(user, user_match, valid_room):
    position = user.position  # 해당 사용자 포지션

    room_match = valid_room.prefetch_related("match_set")
    matching_data = room_match.filter(match__position=position)

    for room in valid_room:
        current_position = matching_data.filter(id=room.id).count()
        max_position = getattr(room, f"max_{position}")

        if max_position - current_position:
            user_match.room = room
            user_match.save()

            return Response({"success": 1, "data": "사용자 채팅방 입장"}, status=status.HTTP_200_OK)

    return Response({"success": 1, "data": "사용자 매칭풀 입장"}, status=status.HTTP_200_OK)


def random_matching(user):
    matches = Match.objects.filter(room=None).all()  # 매칭풀 == 방이 지정되지 않은 사용자들

    position_config = {position: matches.filter(position=position).count() for position in POSITIONS}

    if not (position_config["designer"] and position_config["backend"]):
        # 디자이너와 백엔드는 필수
        return Response({"success": 1, "data": "필수 조건 불만족"}, status=status.HTTP_200_OK)

    if not (position_config["frontend"] or position_config["iosdev"] or position_config["aosdev"]):
        # 사용자 환경 작업자 1명은 필수
        return Response({"success": 1, "data": "최소 구성 인원 불만족"}, status=status.HTTP_200_OK)

    return Response({"success": 1, "data": "방 생성해도 됨"}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def create_room_view(request):
    user = request.user

    is_user_matching = Match.objects.filter(user=user)  # 사용자가 매칭풀에 있는 지 여부

    if is_user_matching:
        # 사용자가 매칭풀에 있는 경우
        matching_data = is_user_matching[0]
    else:
        matching_data = Match.objects.create(user=user, position=user.position)

    serializer = CreateRoomSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        room = Room.objects.filter(room_hash=serializer.data.room_hash)[0]

        matching_data.room = room
        matching_data.save()

        user_matching(room)

        return Response(
            {
                "success": 1,
                "data": {
                    "room_hash": serializer.data.room_hash,
                    "activate": serializer.data.activate,
                    "room_name": serializer.data.room_name,
                },
            },
            status=status.HTTP_200_OK,
        )

    print(serializer.errors.keys())
    raise exc.ParseError(code="CREATE-ROOM-ERROR", detail="채팅방 생성 중 오류 발생")


def user_matching(room):
    matches = Match.objects.filter(room=None)  # 매칭풀 == 방이 지정되지 않은 사용자들

    matching_table = {f"max_{position}": getattr(room, f"max_{position}") for position in POSITIONS}

    for match in matches:
        position = match.position
        max_position = f"max_{position}"
        valid_room = matching_table[max_position]

        if valid_room:
            # 매칭 가능 상태
            match.room = room
            matching_table[max_position] -= 1

    if not any(matching_table.values()):
        # 해당 방에 모두 매칭됨
        room.deleted_yn = 1
        room.save()


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def update_room_view(request):
    room = Room.objects.prefetch_related("match_set").get(match__user_id=request.user.id)

    serializer = UpdateRoomSerializer(instance=room, data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response({"success": 1, "data": serializer.data}, status=status.HTTP_200_OK)

    print(serializer.errors.keys())
    raise exc.ParseError(code="UPDATE-ROOM-ERROR", detail="채팅방 정보 수정 중 오류 발생")


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_room_view(request):
    user_has_room = Match.objects.values("room_hash").filter(user=request.user)

    if user_has_room:
        room_hash = user_has_room[0].get("room_hash")

        user_match = User.objects.prefetch_related("match_set")

        users = list(user_match.filter(room__room_hash=room_hash).values())

        return Response({"success": 1, "data": {"room_hash": room_hash, "users": users}}, status=status.HTTP_200_OK)

    return Response({"success": 1, "data": "해당 사용자가 속한 채팅방이 없음"}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_messages_view(request):
    room_hash = request.data.get("room_hash")
    page_index = request.data.get("page_index")

    message_object = (
        Message.objects.values("nickname", "content", "created_at", "updated_at")
        .order_by("-created_at")
        .filter(user=request.user, room=Room.objects.get(room_hash=room_hash))
    )

    message_paginator = Paginator(message_object, 30)

    messages = message_paginator.get_page(page_index)
    max_loading = message_paginator.end_index()

    return Response(
        {"success": 1, "data": {"max_loading": max_loading, "messages": messages}}, status=status.HTTP_200_OK
    )
