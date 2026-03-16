from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<lobby_name>[\w-]+)/$', consumers.LobbyChatConsumer.as_asgi()),
]