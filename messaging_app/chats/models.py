#!/usr/bin/env python3
"""Models for the chats app."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from typing import Optional


class User(AbstractUser):
    """Custom user model extending Django's AbstractUser."""
    bio = models.TextField(blank=True, null=True, help_text="Optional biography for the user.")
    profile_image = models.URLField(blank=True, null=True, help_text="URL to profile picture.")

    def __str__(self) -> str:
        return self.username


class Conversation(models.Model):
    """Model representing a conversation between users."""
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"Conversation #{self.pk} with {self.participants.count()} participants"


class Message(models.Model):
    """Message model containing sender, conversation, content, and timestamp."""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"Message from {self.sender} at {self.timestamp}"
