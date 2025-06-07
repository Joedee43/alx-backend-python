from django.http import HttpResponseForbidden
from datetime import datetime, time

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