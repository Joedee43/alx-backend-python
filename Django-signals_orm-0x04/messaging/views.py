from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch
from .models import Message, User

def conversation_thread(request, message_id):
    # Get the root message with all replies efficiently
    message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver')
                      .prefetch_related(
                          Prefetch('replies', 
                                  queryset=Message.objects.select_related('sender', 'receiver')
                                  .order_by('timestamp'))
                      ),
        pk=message_id
    )
    
    # Get the complete thread
    thread = message.get_thread()
    
    return render(request, 'messaging/thread.html', {
        'root_message': message,
        'thread': thread
    })