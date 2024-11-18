from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
import json
from .models import *


class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        print(self.user)
        print(self.chatroom_name)
        self.chatroom = get_object_or_404(ChatGroup, group_name=self.chatroom_name)
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']

        print(body)


class OnlineStatusConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.group_name = 'online-status'
        self.group = get_object_or_404(ChatGroup, group_name=self.group_name)

        if self.user not in self.group.users_online.all():
            self.group.users_online.add(self.user)

        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )

        self.accept()
        self.online_status()

    def disconnect(self, close_code):
        if self.user in self.group.users_online.all():
            self.group.users_online.remove(self.user)

        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )
        self.online_status()

    def online_status(self):
        event = {
            'type': 'online_status_handler'
        }
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, event
        )

    def online_status_handler(self, event):
        online_users = self.group.users_online.exclude(id=self.user.id)
        public_chat_users = ChatGroup.objects.get(
            group_name='public-chat').users_online.exclude(id=self.user.id)

        my_chats = self.user.chat_groups.all()
        private_chats_with_users = [chat for chat in my_chats.filter(
            is_private=True) if chat.users_online.exclude(id=self.user.id)]
        group_chats_with_users = [chat for chat in my_chats.filter(
            groupchat_name__isnull=False) if chat.users_online.exclude(id=self.user.id)]

        if public_chat_users or private_chats_with_users or group_chats_with_users:
            online_in_chats = True
        else:
            online_in_chats = False

        context = {
            'online_users': online_users,
            'online_in_chats': online_in_chats,
            'public_chat_users': public_chat_users,
            'user': self.user
        }
        html = render_to_string(
            "a_rtchat/partials/online_status.html", context=context)
        self.send(text_data=html)
