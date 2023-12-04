from django.contrib.auth.models import User
from django.db import models

class Conversation(models.Model):
    members = models.ManyToManyField(User, through='Member', related_name='conversations_as_member')
    type = models.CharField(max_length=5, choices=[("chat", "Chat"), ("group", "Group")], default="chat")
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='conversations_as_creator')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='members')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receivers = models.ManyToManyField(User, through='Receiver', related_name='received_messages')
    attachment_picture = models.ImageField(null=True, blank=True, upload_to='picture/')
    attachment_video = models.FileField(null=True, blank=True, upload_to='video/')
    text = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Receiver(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    attachment_picture = models.ImageField(null=True, blank=True, upload_to='picture/')
    attachment_video = models.FileField(null=True, blank=True, upload_to='video/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    received_at = models.DateTimeField(auto_now_add=True)
