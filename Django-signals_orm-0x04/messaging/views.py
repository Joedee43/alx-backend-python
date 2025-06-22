from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.http import require_POST

User = get_user_model()

@require_POST
@login_required
def delete_user(request):
    user = request.user
    user.delete()
    messages.success(request, 'Your account has been successfully deleted.')
    return redirect('home')  # Replace 'home' with your actual home URL name