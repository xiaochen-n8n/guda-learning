from django.urls import re_path
from . import consumers

# 对外暴露端口
websocket_urlpatterns = [
    re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()),
]