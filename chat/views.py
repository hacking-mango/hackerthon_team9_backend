import json

from django.shortcuts import render
from django.utils.safestring import mark_safe
from rest_framework import exceptions as exc
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user.models import User

from .models import Match, Room

POSITIONS = ["planner", "designer", "frontend", "backend", "aosdev", "iosdev"]


def index(request):
    return render(request, "chat/index.html", {})


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name_json": mark_safe(json.dumps(room_name))})


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def matching_view(request):
    user = request.user
    valid_data = Match.objects.filter(room__delete_yn=0)  # room delete_yn = 매칭 완료 여부

    if valid_data:
        # 매칭 완료가 되지 않은 방이 있다면
        room_matching(user, valid_data)

    random_matching(user)


def room_matching(user, valid_data):
    position = user.position  # 해당 사용자 포지션
    max_position = f"room__max_{position}"  # 채팅방의 position 최대 인원 수를 구하기 위한 필터 키

    valid_matches = valid_data.filter(position=position)  # position 의 매칭 현황을 구히기 위한 변수
    matching_data = valid_matches.values(max_position, "room_id")  # 매칭을 위한 기준 쿼리셋

    already_checked = []  # 이미 확인한 방

    for matching in matching_data:
        room_id = matching["room_id"]  # 해당 매칭 정보의 방 pk

        if room_id in already_checked:  # 이미 확인했다면, 다음 정보로
            continue

        user_in_room = matching_data.filter(room_id=matching["room_id"]).count()

        if matching[max_position] - user_in_room > 0:
            Match.create(user=user, room=room, position=position)
            return Response({"success": 1, "data": "매칭 성공!"}, status=status.HTTP_200_OK)

        already_checked.append(room_id)

    Match.create(user=user, position=position)  # 매칭풀로 이동

    return Response({"success": 1, "data": "매칭 실패.."}, status=status.HTTP_200_OK)


def random_matching(user):
    queue_of_user, new_matching = Match.objects.get_or_create(user=user, position=user.position)
    # 대기 중인 사용자, 매칭이 새로 생성된 지 여부

    if not new_matching:
        # 매칭이 새로 생성되지 않음 == 기존에 매칭이 있음
        raise exc.ParseError(code="MATCHING_ALREADY_EXISTS", detail="이미 매칭풀에 존재하는 사용자")

    matches = Match.objects.filter(room=None).all()  # 매칭풀 == 방이 지정되지 않은 사용자들

    position_config = {position: matches.filter(position=position).count() for position in POSITIONS}

    if not (position_config["designer"] and position_config["backend"]):
        # 디자이너와 백엔드는 필수
        return Response({"success": 1, "data": "필수 조건 불만족"}, status=status.HTTP_200_OK)

    if not (position_config["frontend"] or position_config["iosdev"] or position_config["aosdev"]):
        # 사용자 환경 작업자 1명은 필수
        return Response({"success": 1, "data": "최소 구성 인원 불만족"}, status=status.HTTP_200_OK)

    return Response({"success": 1, "data": "방 생성해도 됨"}, status=status.HTTP_200_OK)
