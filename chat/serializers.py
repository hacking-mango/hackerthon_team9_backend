from rest_framework import serializers

from .models import Room


class CreateRoomSerializer(serializers.ModelSerializer):

    # 채팅방을 만드려면, 해시값 관련 규칙이 필요함
    # def create(self, validated_data):
    # room = Room.objects.create(
    # room_hash=validated_data["room_hash"],
    # activate=validated_data["activate"],
    # room_name=validated_data["room_name"],
    # max_planner=validated_data["max_planner"],
    # max_designer=validated_data["max_designer"],
    # max_frontend=validated_data["max_frontend"],
    # max_backend=validated_data["max_backend"],
    # max_aosdev=validated_data["max_aosdev"],
    # max_iosdev=validated_data["max_iosdev"],
    # )
    # room.save()
    # return room

    class Meta:
        model = Room
        fields = [
            "room_hash",
            "activate",
            "room_name",
            "max_planner",
            "max_designer",
            "max_frontend",
            "max_backend",
            "max_aosdev",
            "max_iosdev",
        ]


class UpdateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            "activate",
            "room_name",
            "max_planner",
            "max_designer",
            "max_frontend",
            "max_backend",
            "max_aosdev",
            "max_iosdev",
        ]
