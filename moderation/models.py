from django.db import models

# Create your models here.
# moderation/models.py
from django.db import models
from django.conf import settings
from interactions.models import Report

class ModerationLog(models.Model):
    ACTION_CHOICES = [
        ('delete_post',   'Xóa bài viết'),
        ('lock_topic',    'Khóa chủ đề'),
        ('warn_user',     'Cảnh báo người dùng'),
        ('ban_user',      'Khóa tài khoản'),
        ('resolve_report','Xử lý báo cáo'),
        ('dismiss_report','Bỏ qua báo cáo'),
    ]

    moderator  = models.ForeignKey(
                    settings.AUTH_USER_MODEL,
                    on_delete=models.SET_NULL,
                    null=True,
                    related_name='moderation_logs',
                    verbose_name='Người kiểm duyệt')
    action     = models.CharField(max_length=30, choices=ACTION_CHOICES,
                    verbose_name='Hành động')
    report     = models.ForeignKey(
                    Report,
                    on_delete=models.SET_NULL,
                    null=True, blank=True,
                    related_name='logs',
                    verbose_name='Báo cáo liên quan')
    note       = models.TextField(blank=True, verbose_name='Ghi chú')
    created_at = models.DateTimeField(auto_now_add=True,
                    verbose_name='Thời gian xử lý')

    class Meta:
        verbose_name        = 'Nhật ký kiểm duyệt'
        verbose_name_plural = 'Nhật ký kiểm duyệt'
        ordering            = ['-created_at']

    def __str__(self):
        return f'{self.moderator} - {self.get_action_display()} - {self.created_at:%d/%m/%Y %H:%M}'