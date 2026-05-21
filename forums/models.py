from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class Forum(models.Model):
    forum_name  = models.CharField(max_length=100, verbose_name='Tên chuyên mục')
    description = models.TextField(null=True, blank=True,
                                   verbose_name='Mô tả')
    icon_url    = models.CharField(max_length=255, null=True, blank=True,
                                   verbose_name='Biểu tượng (CSS class hoặc URL)')
    created_by  = models.ForeignKey(
                    settings.AUTH_USER_MODEL,
                    on_delete=models.SET_NULL,   # bảng 2.9: SET NULL
                    null=True, blank=True,
                    related_name='created_forums',
                    verbose_name='Người tạo')
    created_at  = models.DateTimeField(auto_now_add=True)
    is_active   = models.BooleanField(default=True,  # bảng 2.4
                                      verbose_name='Đang hoạt động')
    
    class Meta:
        verbose_name        = 'Chuyên mục'
        verbose_name_plural = 'Chuyên mục'
        ordering            = ['forum_name']

    def __str__(self):
        return self.forum_name

    def topic_count(self):
        return self.topics.count()

    def total_views(self):
        return sum(t.view_count for t in self.topics.all())