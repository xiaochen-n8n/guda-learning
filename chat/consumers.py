import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Profile

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        def get_display_name(user):
            try:
                return Profile.objects.get(user=user).nickname
            except Profile.DoesNotExist:
                return user.username

        self.room_group_name = "chat_room"
        self.username = await sync_to_async(get_display_name)(self.scope["user"])

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({"message": f"✅ {self.username} 已连接！"}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat.message", "username": self.username, "message": message},
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": f"{event['username']}: {event['message']}"
        }))
