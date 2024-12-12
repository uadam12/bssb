from django.db.models import Q
from django.http import HttpRequest
from main.models import Notification

def get_notifications(user, limit:int=0):
    if not user.is_authenticated:
        notifications = Notification.objects.filter(visibility='public')
        if limit: notifications = notifications[:limit]
        
        messages = [{
            'message': notification.message,
            'read': True
        } for notification in notifications]

        return {
            'notification': {
                'unread': 0,
                'messages': messages
            }
        }
    
    messages, unread = [], 0
    notifications = Notification.objects.filter(
        Q(visibility__in=['public', 'members']) |
        Q(visibility='selected', users=user)
    ).distinct()
    
    for notification in notifications:
        read = user.last_time_read_notifications > notification.notified_at

        if not read:
            unread += 1

        messages.append({
            'message': notification.message,
            'read': read
        })
        
    if limit: messages = messages[:5]

    return {
        'notification': {
            'unread': unread,
            'messages': messages
        }
    }

def notifications(request:HttpRequest):
    return get_notifications(request.user, 5)