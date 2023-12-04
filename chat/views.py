from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Member, Message, Receiver
from .serializers import ConversationSerializer, MessageSerializer, MemberSerializer, ReceiverSerializer


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
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]


class LeaveChatroomView(generics.DestroyAPIView):
    queryset = Member.objects.all()
    permission_classes = [IsAuthenticated]


class SendMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(sender=user)


class ListMessagesView(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]


class ReadMessageView(generics.UpdateAPIView):
    queryset = Receiver.objects.all()
    serializer_class = ReceiverSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

