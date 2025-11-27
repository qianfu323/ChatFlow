from django.urls import path
from chat.api import *

# URL patterns for chat app
urlpatterns = [
    path('user/login', user_login, name='login'),
    path('user/register', user_register, name='register'),
    path('room', room, name='room'), # room handler
    path('message', message, name='message'), # room handler
]
