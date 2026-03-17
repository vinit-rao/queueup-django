import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Post, Message

active_lobby_users = {}


class LobbyChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.lobby_name = self.scope['url_route']['kwargs']['lobby_name']
        self.room_group_name = f"chat_{self.lobby_name}"
        self.user = self.scope["user"]

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        if self.user.is_authenticated:
            if self.room_group_name not in active_lobby_users:
                active_lobby_users[self.room_group_name] = set()

            active_lobby_users[self.room_group_name].add(self.user.username)

            await self.broadcast_user_list()

    async def disconnect(self, close_code):
        if self.user.is_authenticated and self.room_group_name in active_lobby_users:
            active_lobby_users[self.room_group_name].discard(self.user.username)

            if not active_lobby_users[self.room_group_name]:
                del active_lobby_users[self.room_group_name]

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        await self.broadcast_user_list()

    async def broadcast_user_list(self):
        """Helper to send the current list of names to the whole group"""
        users = list(active_lobby_users.get(self.room_group_name, []))
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_list_update',
                'users': users
            }
        )

    async def user_list_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user_list',
            'users': event['users']
        }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'user': event['user']
        }))

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope["user"]

        if user.is_authenticated:
            await self.save_message(user, self.lobby_name, message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': user.username
                }
            )

    @database_sync_to_async
    def save_message(self, user, slug, content):
        try:
            post = Post.objects.get(slug=slug)
            Message.objects.create(user=user, post=post, content=content)
        except Post.DoesNotExist:
            pass