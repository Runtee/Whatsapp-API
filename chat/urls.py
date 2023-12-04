from django.urls import path
from .views import CreateChatroomView, ListChatroomsView, LeaveChatroomView, SendMessageView, ListMessagesView, JoinChatroomView

urlpatterns = [
    path('create_chatroom/', CreateChatroomView.as_view(), name='create_chatroom'),
    path('list_chatrooms/', ListChatroomsView.as_view(), name='list_chatrooms'),
    path('leave_chatroom/<int:pk>/', LeaveChatroomView.as_view(), name='leave_chatroom'),
    path('send_message/', SendMessageView.as_view(), name='send_message'),
    path('list_messages/', ListMessagesView.as_view(), name='list_messages'),
    path('join_chatroom/', JoinChatroomView.as_view(), name='join_chatroom'),

]
