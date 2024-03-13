# consumers.py in your chat app

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, ChatRoom
from asgiref.sync import sync_to_async
import bleach

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Save the message to the database
        await self.save_message(self.room_id, self.scope["user"], message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.scope["user"].username,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
        }))

    @sync_to_async
    def save_message(self, room_id, user, message):
        room = ChatRoom.objects.get(id=room_id)    
    
        # Define the list of allowed tags and attributes
        allowed_tags = ['p', 'b', 'i', 'u', 'em', 'strong', 'a', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        # Define allowed attributes, and optionally allow 'style' for all tags
        allowed_attrs = {
            'a': ['href', 'title'],
            '*': ['style']  # This allows 'style' attribute for all tags
        }
        
        # Specify allowed CSS properties within 'style' attribute
        # If you want to allow specific CSS styles, you would need to list them here
        allowed_styles = [
            'color', 
            'font-weight', 
            'text-decoration', 
            'font-style',
            'font-family',
            'text-align',
            'background-color'
        ]
        
        # Sanitize the message content with the updated rules
        sanitized_message = message #bleach.clean(message, tags=allowed_tags, attributes=allowed_attrs,  strip=True)
    
        Message.objects.create(room=room, user=user, message=sanitized_message)
