import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Conversation, Message, Receiver

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        event_type = data.get('type')

        if event_type == 'message':
            await self.handle_chat_message(data["message"])
        elif event_type == 'typing':
            await self.handle_typing_notification(data["message"])

    @database_sync_to_async
    def get_conversation(self, room_id):
        try:
            conversation = Conversation.objects.get(id=room_id)
            return conversation
        except Conversation.DoesNotExist:
            return None

    @database_sync_to_async
    def create_message(self, conversation, sender, message_content, attachment_picture, attachment_video):
        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            text=message_content,
            attachment_picture=attachment_picture,
            attachment_video=attachment_video
        )

        # Exclude the sender from the list of receivers
        receivers = conversation.members.exclude(id=sender.id)
        for receiver in receivers:
            Receiver.objects.create(message=message, user=receiver, attachment_picture=attachment_picture,
                                    attachment_video=attachment_video)

        return message

    async def handle_chat_message(self, data):
        conversation_id = data['conversation']
        message_content = data.get('text', '')
        sender_id = data['sender']
        attachment_picture = data.get('attachment_picture', None)
        attachment_video = data.get('attachment_video', None)
        try:
            conversation = await self.get_conversation(conversation_id)
            if conversation is None:
                raise ValueError("Conversation does not exist.")

            sender = User.objects.get(id=sender_id)
            message = await self.create_message(conversation, sender, message_content, attachment_picture, attachment_video)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                }
            )
        except Exception as e:
            pass

    async def handle_typing_notification(self, data):
        conversation_id = data.get('conversation')
        sender_id = data.get('sender')
        try:
            conversation = await self.get_conversation(conversation_id)
            if conversation is None:
                raise ValueError("Conversation does not exist.")

            # Broadcast the typing status to other users in the room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_notification',
                    'sender': sender_id,
                }
            )
        except Exception as e:
            # Log the exception or handle it as needed
            pass

    async def chat_message(self, event):
        message = event['message']
        # Send the chat message to the WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': {
                'id': message.id,
                'conversation': message.conversation.id,
                'sender_id': message.sender_id,
                'message': message.text,
                'attachment_picture': message.attachment_picture,
                'attachment_video' : message.attachment_video,
                'created_at': message.created_at.isoformat(),
            }
        }))

    async def typing_notification(self, event):
        sender_id = event['sender_id']
        # Send the typing notification to the WebSocket
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'sender': sender_id,
        }))
