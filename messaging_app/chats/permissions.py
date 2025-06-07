#!/usr/bin/env python3
"""Custom permissions for the messaging app."""

from rest_framework import permissions
from .models import Conversation, Message
from typing import Any


class IsConversationParticipant(permissions.BasePermission):
    """Permission to allow access only to conversation participants."""

    def has_object_permission(self, request: Any, view: Any, obj: Any) -> bool:
        """Check if the user is a participant in the conversation or message."""
        if isinstance(obj, Conversation):
            return request.user in (obj.user1, obj.user2)
        elif isinstance(obj, Message):
            return request.user in (obj.conversation.user1, obj.conversation.user2)
        return False