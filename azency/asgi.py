# yourproject/asgi.py

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from django.urls import path
from chat.consumers import ChatConsumer  # Update with your app name and consumer
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'azency.settings')
django.setup()  

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/chat/rooms/<int:room_id>/", ChatConsumer.as_asgi()),  # WebSocket URL for chat
        ])
    ),
})
