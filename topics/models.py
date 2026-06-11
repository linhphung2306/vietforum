from django.db import models
from django.conf import settings
from forums.models import Forum
from cloudinary.models import CloudinaryField

class Topic(models.Model):
    forum      = models.ForeignKey(Forum, on_delete=models.CASCADE,
                   related_name='topics', verbose_name='Chuyên mục')
    author     = models.ForeignKey(settings.AUTH_USER_MODEL,
                   on_delete=models.SET_NULL,
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
    topic          = models.ForeignKey(Topic, on_delete=models.CASCADE,
                       related_name='posts', verbose_name='Chủ đề')
    author         = models.ForeignKey(settings.AUTH_USER_MODEL,
                       on_delete=models.SET_NULL,
                       null=True, related_name='posts',
                       verbose_name='Người đăng')
    parent_post    = models.ForeignKey('self', on_delete=models.SET_NULL,
                       null=True, blank=True,
                       related_name='replies',
                       verbose_name='Trả lời bài')
    content        = models.TextField(verbose_name='Nội dung')
    is_deleted     = models.BooleanField(default=False,
                       verbose_name='Đã xóa')
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name        = 'Bài viết'
        verbose_name_plural = 'Bài viết'
        ordering            = ['created_at']

    def __str__(self):
        return f'Post #{self.pk} by {self.author}'


class Attachment(models.Model):
    FILE_TYPE_CHOICES = [
        ('image', 'Ảnh'),
        ('file',  'File'),
    ]
    topic     = models.ForeignKey(Topic, on_delete=models.CASCADE,
                  null=True, blank=True,
                  related_name='attachments', verbose_name='Chủ đề')
    post      = models.ForeignKey(Post, on_delete=models.CASCADE,
                  null=True, blank=True,
                  related_name='attachments', verbose_name='Bài viết')
    author    = models.ForeignKey(settings.AUTH_USER_MODEL,
                  on_delete=models.SET_NULL, null=True,
                  verbose_name='Người đăng')
    file      = CloudinaryField('file', resource_type='auto',
                  null=True, blank=True)
    file_name = models.CharField(max_length=255, blank=True,
                  verbose_name='Tên file')
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES,
                  default='file', verbose_name='Loại file')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Tệp đính kèm'
        verbose_name_plural = 'Tệp đính kèm'

    def __str__(self):
        return f'{self.file_name} by {self.author}'

    def is_image(self):
        return self.file_type == 'image'

    def get_download_url(self):
        if self.file:
            return self.file.url.replace('/upload/', '/upload/fl_attachment/')
        return ''