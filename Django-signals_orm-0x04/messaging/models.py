from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, 
                                     null=True, blank=True, related_name='replies')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    last_edited = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['sender', 'receiver']),
            models.Index(fields=['parent_message']),
        ]

    def __str__(self):
        return f"Message {self.id} from {self.sender}"

    @classmethod
    def get_conversation(cls, user1, user2):
        """Get all messages between two users with optimized queries"""
        return cls.objects.filter(
            Q(sender=user1, receiver=user2) | Q(sender=user2, receiver=user1)
        ).select_related('sender', 'receiver').prefetch_related('replies')

    def get_thread(self):
        """Get complete thread with all replies"""
        return Message.objects.filter(
            Q(pk=self.pk) | Q(parent_message=self)
        ).select_related('sender', 'receiver').order_by('timestamp')