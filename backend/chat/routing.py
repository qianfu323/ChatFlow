from django.urls import path
from . import consumers

# WebSocket URL routing
websocket_urlpatterns = [
    path('ws/chat/<str:room_id>/', consumers.ChatConsumer.as_asgi()),
]