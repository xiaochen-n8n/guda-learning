import json
import random
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "chat_room"
        self.username = f"User{random.randint(1000, 9999)}"

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
        # 广播到 Redis group
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat.message", "username": self.username, "message": message},
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": f"{event['username']}: {event['message']}"
        }))