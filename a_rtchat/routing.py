from django.urls import path, re_path
from .consumers import *

websocket_urlpatterns = [
    path("ws/chatroom/<chatroom_name>/", ChatroomConsumer.as_asgi()),
    path("ws/test/", TestConsumer.as_asgi()),
]
