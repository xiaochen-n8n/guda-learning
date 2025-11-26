import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Profile
from django.conf import settings
from redis.asyncio import Redis

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
        host, port = settings.CHANNEL_LAYERS["default"]["CONFIG"]["hosts"][0]
        self.redis = Redis(host=host, port=port, decode_responses=True)
        self.presence_key = f"presence:{self.room_group_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.redis.sadd(self.presence_key, self.channel_name)
        count = await self.redis.scard(self.presence_key)
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat.join", "username": self.username}
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat.count", "count": count}
        )

    async def disconnect(self, close_code):
        if hasattr(self, "redis"):
            await self.redis.srem(self.presence_key, self.channel_name)
            count = await self.redis.scard(self.presence_key)
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "chat.leave", "username": self.username}
            )
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "chat.count", "count": count}
            )
            await self.redis.close()
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat.message", "username": self.username, "message": message},
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"kind": "chat", "message": f"{event['username']}: {event['message']}"}))

    async def chat_join(self, event):
        await self.send(text_data=json.dumps({"kind": "system", "message": f"{event['username']} 已加入"}))

    async def chat_leave(self, event):
        await self.send(text_data=json.dumps({"kind": "system", "message": f"{event['username']} 已离开"}))

    async def chat_count(self, event):
        await self.send(text_data=json.dumps({"kind": "count", "count": event["count"]}))
