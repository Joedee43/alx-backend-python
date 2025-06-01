#!/usr/bin/env python3
"""Views for the chats app."""

from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import User, Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django_filters.rest_framework import DjangoFilterBackend


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing conversations."""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['participants']

    def get_queryset(self):
        # Limit to conversations the authenticated user participates in
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        participant_ids = request.data.get('participants', [])
        if not participant_ids:
            return Response({"error": "At least one participant is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Add current user if not in the list
        participants = User.objects.filter(id__in=participant_ids)
        if request.user.id not in participant_ids:
            participants |= User.objects.filter(id=request.user.id)

        conversation = serializer.save()
        conversation.participants.set(participants)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for managing messages."""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['conversation']
    ordering_fields = ['timestamp']

    def get_queryset(self):
        # Return messages only from conversations the user is part of
        return Message.objects.filter(conversation__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        conversation_id = request.data.get('conversation')
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        if not conversation.participants.filter(id=request.user.id).exists():
            return Response({"error": "User is not a participant in this conversation."}, status=status.HTTP_403_FORBIDDEN)

        message = serializer.save(sender=request.user)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
