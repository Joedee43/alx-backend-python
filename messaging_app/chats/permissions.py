from rest_framework import permissions
from .models import Conversation, Message
from typing import Any


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow:
    - Authenticated users
    - Participants of a conversation to access messages
    """
    
    def has_permission(self, request, view):
        # Allow only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # For Conversation objects
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()
        
        # For Message objects
        elif isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()
        
        return False