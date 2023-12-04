from rest_framework import serializers
from .models import Conversation, Member, Message, Receiver

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'
        extra_kwargs = {
            'created_by': {'read_only': True}
        }

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class ReceiverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receiver
        fields = '__all__'