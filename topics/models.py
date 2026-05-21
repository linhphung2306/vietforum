from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from forums.models import Forum

class Topic(models.Model):
    # Bảng 2.5: topic_id, forum_id, user_id, title, content,
    #            view_count, is_pinned, is_locked, created_at, updated_at
    forum      = models.ForeignKey(Forum, on_delete=models.CASCADE,
                   related_name='topics', verbose_name='Chuyên mục')
    author     = models.ForeignKey(settings.AUTH_USER_MODEL,
                   on_delete=models.SET_NULL,  # bảng 2.9: SET NULL
                   null=True, related_name='topics',
                   verbose_name='Người tạo')
    title      = models.CharField(max_length=255, verbose_name='Tiêu đề')
    content    = models.TextField(verbose_name='Nội dung')
    view_count = models.PositiveIntegerField(default=0,
                   verbose_name='Lượt xem')
    is_pinned  = models.BooleanField(default=False,
                   verbose_name='Ghim')
    is_locked  = models.BooleanField(default=False,
                   verbose_name='Khóa')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name        = 'Chủ đề'
        verbose_name_plural = 'Chủ đề'
        ordering            = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title

    def post_count(self):
        return self.posts.filter(is_deleted=False).count()
class Post(models.Model):
    # Bảng 2.6: post_id, topic_id, user_id, parent_post_id,
    #            content, is_deleted, created_at, updated_at
    topic          = models.ForeignKey(Topic, on_delete=models.CASCADE,
                       related_name='posts', verbose_name='Chủ đề')
    author         = models.ForeignKey(settings.AUTH_USER_MODEL,
                       on_delete=models.SET_NULL,  # bảng 2.9: SET NULL
                       null=True, related_name='posts',
                       verbose_name='Người đăng')
    parent_post    = models.ForeignKey('self', on_delete=models.SET_NULL,
                       null=True, blank=True,
                       related_name='replies',
                       verbose_name='Trả lời bài')  # trích dẫn
    content        = models.TextField(verbose_name='Nội dung')
    is_deleted     = models.BooleanField(default=False,
                       verbose_name='Đã xóa')  # soft delete — bảng 2.6
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        verbose_name        = 'Bài viết'
        verbose_name_plural = 'Bài viết'
        ordering            = ['created_at']

    def __str__(self):
        return f'Post #{self.pk} by {self.author}'