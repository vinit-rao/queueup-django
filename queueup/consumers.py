import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Post, Message

class LobbyChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # We are using the Post's slug as the lobby_name
        self.lobby_name = self.scope['url_route']['kwargs']['lobby_name']
        self.room_group_name = f"chat_{self.lobby_name}"

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket (Frontend)
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope["user"]

        # Only process if the user is authenticated
        if user.is_authenticated:
            # Save the message to the database first
            await self.save_message(user, self.lobby_name, message)

            # Broadcast the message to the room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': user.username
                }
            )

    # Receive message from room group (Backend broadcasting to all clients)
    async def chat_message(self, event):
        message = event['message']
        username = event['user']

        # Send message back to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': username
        }))

    # Synchronous database wrapper to save the message to the specific Post
    @database_sync_to_async
    def save_message(self, user, slug, content):
        try:
            # Find the post by its slug
            post = Post.objects.get(slug=slug)
            # Create and save the message linked to that post
            Message.objects.create(user=user, post=post, content=content)
        except Post.DoesNotExist:
            # Failsafe in case someone connects to a non-existent slug
            pass