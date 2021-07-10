import json

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer

from user.models import User

from .models import Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):  # 사용자가 접속했을 때 동작하는 함수
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

    @database_sync_to_async
    def create_message(data):
        author = User.objects.filter(email=data["from"])[0]

        message = Message.objects.create(user=author, content=data["message"])

        return message

    def disconnect(self, close_code):  # 사용자가 방에서 떠났을 때 동작하는 함수
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    def chat_message(self, event):  # 실제로 메시지를 전송하는 함수
        message = event["message"]
        self.send(text_data=json.dumps(message))

    def receive(self, text_data):  # 채팅방에 메시지가 전파되었을 때 동작하는 함수
        data = json.loads(text_data)

        message = create_message(data)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": {
                    "message": {
                        "nickname": message.user.nickname,
                        "content": message.content,
                        "created_at": message.created_at,
                        "updated_at": message.updated_at,
                    },
                },
            },
        )
