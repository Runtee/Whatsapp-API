from django.urls import path
from .views import (
    CreateChatroomView,
    JoinChatroomView,
    ListChatroomsView,
    LeaveChatroomView,
    SendMessageView,
    ListMessagesView,
    ListConversationMessagesView,
    ReadMessageView,
)

urlpatterns = [
    path('create-chatroom/', CreateChatroomView.as_view(), name='create-chatroom'),
    path('join-chatroom/', JoinChatroomView.as_view(), name='join-chatroom'),
    path('list-chatrooms/', ListChatroomsView.as_view(), name='list-chatrooms'),
    path('leave-chatroom/<int:conversation_id>/', LeaveChatroomView.as_view(), name='leave-chatroom'),
    path('send-message/', SendMessageView.as_view(), name='send-message'),
    path('list-messages/', ListMessagesView.as_view(), name='list-messages'),
    path('list-conversation-messages/<int:conversation_id>/', ListConversationMessagesView.as_view(), name='list-conversation-messages'),
    path('read-message/', ReadMessageView.as_view(), name='read-message'),
]
