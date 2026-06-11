from django.db import models
from django.conf import settings
from topics.models import Post


class Vote(models.Model):
    VOTE_TYPE = [('like', 'Like'), ('dislike', 'Dislike')]
    post       = models.ForeignKey(Post, on_delete=models.CASCADE,
                   related_name='votes', verbose_name='Bài viết')
    user       = models.ForeignKey(settings.AUTH_USER_MODEL,
                   on_delete=models.CASCADE,
                   related_name='votes', verbose_name='Người vote')
    vote_type  = models.CharField(max_length=10, choices=VOTE_TYPE,
                   verbose_name='Loại vote')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name    = 'Vote'
        unique_together = ['post', 'user']

    def __str__(self):
        return f'{self.user} {self.vote_type} post #{self.post_id}'


class Report(models.Model):
    STATUS = [
        ('pending',   'Chờ xử lý'),
        ('resolved',  'Đã xử lý'),
        ('dismissed', 'Bỏ qua'),
    ]
    post        = models.ForeignKey(Post, on_delete=models.CASCADE,
                    related_name='reports', verbose_name='Bài viết')
    reporter    = models.ForeignKey(settings.AUTH_USER_MODEL,
                    on_delete=models.CASCADE,
                    related_name='reports_sent',
                    verbose_name='Người báo cáo')
    reason      = models.TextField(verbose_name='Lý do')
    status      = models.CharField(max_length=20, choices=STATUS,
                    default='pending', verbose_name='Trạng thái')
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                    on_delete=models.SET_NULL,
                    null=True, blank=True,
                    related_name='reports_reviewed',
                    verbose_name='Người xử lý')
    created_at  = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name        = 'Báo cáo vi phạm'
        verbose_name_plural = 'Báo cáo vi phạm'
        ordering            = ['-created_at']

    def __str__(self):
        return f'Báo cáo #{self.pk} - {self.get_status_display()}'