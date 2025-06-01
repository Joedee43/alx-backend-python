# chats/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """Custom user model extending AbstractUser."""
    # Add custom fields here if needed
    pass

class Message(models.Model):
    """Model to represent a chat message."""
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}: {self.content[:30]}"


# chats/admin.py
from django.contrib import admin
from .models import CustomUser, Message
from django.contrib.auth.admin import UserAdmin

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Message)


# chats/views.py
from rest_framework import viewsets
from .models import Message
from .serializers import MessageSerializer
from rest_framework.permissions import IsAuthenticated

class MessageViewSet(viewsets.ModelViewSet):
    """API endpoint for viewing and sending messages."""
    queryset = Message.objects.all().order_by('-timestamp')
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]


# chats/tests.py
from django.test import TestCase
from .models import CustomUser, Message

class MessageModelTest(TestCase):
    def setUp(self):
        self.sender = CustomUser.objects.create_user(username='alice', password='password123')
        self.receiver = CustomUser.objects.create_user(username='bob', password='password123')

    def test_message_creation(self):
        msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Hello Bob!')
        self.assertEqual(msg.content, 'Hello Bob!')
        self.assertEqual(msg.sender.username, 'alice')
        self.assertEqual(msg.receiver.username, 'bob')
