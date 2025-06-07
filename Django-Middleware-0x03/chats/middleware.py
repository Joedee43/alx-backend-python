from django.http import HttpResponseForbidden
from datetime import datetime, time
from django.http import HttpResponseForbidden
from datetime import datetime, timedelta
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_counts = defaultdict(list)
        self.limit = 5  # 5 messages
        self.time_window = 60  # 60 seconds (1 minute)

    def __call__(self, request):
        # Only process POST requests to message endpoints
        if request.method == 'POST' and ('/messages/' in request.path or '/chats/' in request.path):
            ip_address = self.get_client_ip(request)
            now = datetime.now()
            
            # Remove old timestamps
            self.message_counts[ip_address] = [
                ts for ts in self.message_counts[ip_address]
                if now - ts < timedelta(seconds=self.time_window)
            ]
            
            # Check if limit exceeded
            if len(self.message_counts[ip_address]) >= self.limit:
                logger.warning(f"Rate limit exceeded for IP: {ip_address}")
                return HttpResponseForbidden(
                    "Too many messages sent. Please wait 1 minute before sending more.",
                    status=429
                )
            
            # Record new message
            self.message_counts[ip_address].append(now)
        
        return self.get_response(request)

    def get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
    
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define allowed hours (9AM to 6PM)
        self.allowed_start = time(9, 0)  # 9:00 AM
        self.allowed_end = time(18, 0)   # 6:00 PM

    def __call__(self, request):
        current_time = datetime.now().time()
        
        # Check if request path starts with /chats/ (or your chat endpoints)
        if request.path.startswith('/chats/') or request.path.startswith('/api/chats/'):
            if not (self.allowed_start <= current_time <= self.allowed_end):
                return HttpResponseForbidden(
                    "Chat access is only available between 9AM and 6PM"
                )
        
        return self.get_response(request)