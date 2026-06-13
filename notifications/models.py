from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    NOTIF_TYPES = [
        ('reply', 'Có người trả lời chủ đề của bạn'),
        ('vote', 'Có người vote bài viết của bạn'),
        ('report', 'Báo cáo của bạn đã được xử lý'),
    ]

    recipient   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender      = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sent_notifications')
    notif_type  = models.CharField(max_length=20, choices=NOTIF_TYPES)
    topic_id    = models.IntegerField(null=True, blank=True)
    topic_title = models.CharField(max_length=255, null=True, blank=True)
    is_read     = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.notif_type} → {self.recipient.username}"