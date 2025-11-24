from django.urls import path
from chat.api import *

# URL patterns for chat app
urlpatterns = [
    path('user/login', user_login, name='login'),
    path('user/register', user_register, name='register'),
]
