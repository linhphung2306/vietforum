from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(recipient=request.user)
    notifications.filter(is_read=False).update(is_read=True)
    return render(request, 'notifications/list.html', {
        'notifications': notifications
    })

@login_required
def unread_count(request):
    count = Notification.objects.filter(
        recipient=request.user, is_read=False
    ).count()
    return JsonResponse({'count': count})