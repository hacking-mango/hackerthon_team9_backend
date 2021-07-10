import json

from django.shortcuts import render
from django.utils.safestring import mark_safe
from rest_framework import exceptions as exc
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user.models import User

from .models import Match


def index(request):
    return render(request, "chat/index.html", {})


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name_json": mark_safe(json.dumps(room_name))})


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def matching_view(request):
    user = request.user
    queue_of_user, already_in = Match.objects.get_or_create(user=user, position=user.position)

    if already_in:
        raise exc.ParseError(code="MATCHING_ALREADY_EXISTS", detail="이미 매칭풀에 존재하는 사용자")

    matches = Match.objects.filter(room_id=None).all()

    planner = matches.filter(position="planner").count()
    designer = matches.filter(position="designer").count()
    frontend = matches.filter(position="frontend").count()
    backend = matches.filter(position="backend").count()
    aosdev = matches.filter(position="aosdev").count()
    iosdev = matches.filter(position="iosdev").count()

    if not (designer and backend):
        return Response({"success": 1, "data": "필수 조건 불만족"}, status=status.HTTP_200_OK)

    if not (frontend or iosdev or aosdev):
        return Response({"success": 1, "data": "최소 구성 인원 불만족"}, status=status.HTTP_200_OK)

    return Response({"success": 1, "data": "방 생성해도 됨"}, status=status.HTTP_200_OK)
