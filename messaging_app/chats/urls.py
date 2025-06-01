#!/usr/bin/env python3
"""Root URL configuration for messaging_app."""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),
    path('api-auth/', include('rest_framework.urls')),  # ✅ Add this line
]
