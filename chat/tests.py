from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Conversation, Member, Message, Receiver
from django.contrib.auth.models import User

class ChatroomViewsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.conversation = Conversation.objects.create(created_by=self.user)

    def test_leave_chatroom_view(self):
        Member.objects.create(conversation=self.conversation, user=self.user)
        url = reverse('leave-chatroom', kwargs={'conversation_id': self.conversation.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.conversation.members.filter(id=self.user.id).exists())

    def test_leave_chatroom_view_not_member(self):
        url = reverse('leave-chatroom', kwargs={'conversation_id': self.conversation.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'User is not a member of the conversation')

    def test_leave_chatroom_view_unauthenticated(self):
        self.client.logout()
        url = reverse('leave-chatroom', kwargs={'conversation_id': self.conversation.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_read_message_view(self):
        message = Message.objects.create(sender=self.user, conversation=self.conversation)
        receiver = Receiver.objects.create(message=message, user=self.user)
        url = reverse('read-message')
        data = {'conversation_id': self.conversation.id, 'message_ids': [message.id]}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

