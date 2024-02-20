# urls.py in your chat app

from django.urls import path
from . import views

app_name = 'chat'
urlpatterns = [
    # Your other URLs
    path('create/', views.ChatRoomCreateView.as_view(), name='create_room'),
    path('rooms/', views.ChatRoomListView.as_view(), name='room_list'),  # Assuming a view for listing rooms
    path('join/<int:room_id>/', views.join_chat_room, name='join_room'),  # For joining rooms
    path('rooms/<int:room_id>/', views.chat_room, name='chat_room'),  # For the chat room page
]
