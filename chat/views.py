from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.http import JsonResponse
from .models import Conversation, Member, Message, Receiver
from .serializers import ConversationSerializer, MessageSerializer, MemberSerializer, ReceiverSerializer, ReadMessageSerializer

class CreateChatroomView(generics.CreateAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        conversation = serializer.save(created_by=user)
        Member.objects.create(conversation=conversation, user=user)

class JoinChatroomView(generics.CreateAPIView):
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        chatroom_id = self.request.data.get('chatroom_id')

        try:
            conversation = Conversation.objects.get(pk=chatroom_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Chatroom not found"}, status=status.HTTP_404_NOT_FOUND)

        if Member.objects.filter(conversation=conversation, user=user).exists():
            return Response({"error": "User is already a member of this chatroom"}, status=status.HTTP_400_BAD_REQUEST)

        max_member_count = 10
        current_member_count = conversation.members.count()

        if current_member_count >= max_member_count:
            return Response({"error": "Chatroom has reached its maximum member count"}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(conversation=conversation, user=user)

class ListChatroomsView(generics.ListAPIView):
    """
    List the chat rooms the user is in.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return the chat rooms the user is in
        return self.request.user.conversation_set.all()

class LeaveChatroomView(generics.DestroyAPIView):
    """
    Use the conversation id and remove the user from the members folder.
    """
    queryset = Member.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        conversation_id = self.kwargs.get('conversation_id')
        
        # Ensure the user is a member of the conversation
        if not self.request.user.conversation_set.filter(id=conversation_id).exists():
            return Response({"error": "User is not a member of the conversation"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Find the Member instance for the user in the specified conversation
        instance = Member.objects.get(conversation_id=conversation_id, user=self.request.user)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SendMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        conversation = serializer.validated_data['conversation']
        message = serializer.save(sender=user)
        
        # Exclude the sender from the list of receivers
        receivers = conversation.members.exclude(id=user.id)
        for receiver in receivers:
            Receiver.objects.create(message=message, user=receiver)

class ListMessagesView(generics.ListAPIView):
    """
    Get user messages.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return messages sent or received by the user
        return Message.objects.filter(models.Q(sender=self.request.user) | models.Q(receivers=self.request.user)).distinct()

class ListConversationMessagesView(generics.ListAPIView):
    """
    Get conversation messages a user is in.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the conversation id from the URL parameters
        conversation_id = self.kwargs['conversation_id']
        # Return messages from the specified conversation
        return Message.objects.filter(conversation__id=conversation_id)

class ReadMessageView(generics.GenericAPIView):
    """
    Mark messages as read.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ReadMessageSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.mark_messages_as_read(serializer.validated_data)

    def mark_messages_as_read(self, validated_data):
        try:
            # Get the conversation and message IDs from the validated data
            conversation_id = validated_data['conversation_id']
            message_ids = validated_data['message_ids']

            # Ensure the user is a member of the conversation
            if not self.request.user.conversation_set.filter(id=conversation_id).exists():
                return Response({'error': 'User is not a member of the conversation'}, status=status.HTTP_400_BAD_REQUEST)

            # Mark messages as read
            messages_to_mark = Message.objects.filter(id__in=message_ids, conversation__members=self.request.user)
            for message in messages_to_mark:
                receiver = Receiver.objects.get(message=message, user=self.request.user)
                receiver.read = True
                receiver.save()

            return Response({'success': True})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
