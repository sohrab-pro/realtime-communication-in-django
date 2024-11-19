from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='home'),
    path('chat/new-groupchat/', views.create_group_chat, name='new-groupchat'),
    path('chat/edit/<chatroom_name>', views.chatroom_edit, name="edit-chatroom"),
    path('chat/delete/<chatroom_name>', views.chatroom_delete, name="delete-chatroom"),
    path('chat/leave/<chatroom_name>',
         views.leave_chatroom, name="chatroom-leave"),
    path('chat/fileupload/<chatroom_name>', views.chat_file_upload, name="chat-file-upload"),
    path('chat/<username>/', views.get_or_create_chatroom, name='start-chat'),
    path('chat/room/<chatroom_name>/', views.chat_view, name='chatroom'),
]
