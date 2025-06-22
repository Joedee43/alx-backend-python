from django.urls import path
from .views import conversation_thread, delete_user

urlpatterns = [
    path('delete-account/', delete_user, name='delete-account'),
       path('thread/<int:message_id>/', conversation_thread, name='conversation-thread'),
]