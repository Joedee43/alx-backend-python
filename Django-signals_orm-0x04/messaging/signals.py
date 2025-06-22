from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Message, MessageHistory
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from messaging.models import Message, MessageHistory, Notification

User = get_user_model()
@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Clean up all user-related data when a user is deleted
    """
    # Messages where user is sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    
    # Notifications for the user
    Notification.objects.filter(user=instance).delete()
    
    # Message histories where user was the editor
    MessageHistory.objects.filter(editor=instance).delete()

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:  # Only for existing messages (updates)
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:  # Only log if content changed
                MessageHistory.objects.create(
                    message=old_message,
                    content=old_message.content,
                    edited_by=instance.sender
                )
                instance.edited = True
                instance.last_edited = timezone.now()
        except Message.DoesNotExist:
            pass  # New message, nothing to log