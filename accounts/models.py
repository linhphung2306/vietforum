from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    ROLE_CHOICES = [
        ('user',      'Thành viên'),
        ('moderator', 'Kiểm duyệt viên'),
        ('admin',     'Quản trị viên'),
    ]
    display_name = models.CharField(max_length=100, blank=True,
                                    verbose_name='Tên hiển thị')
    avatar_url   = CloudinaryField('Ảnh đại diện', null=True, blank=True)
    role         = models.CharField(max_length=20, choices=ROLE_CHOICES,
                                    default='user', verbose_name='Vai trò')
    bio          = models.TextField(blank=True, verbose_name='Giới thiệu')

    class Meta:
        verbose_name = 'Người dùng'
        verbose_name_plural = 'Người dùng'

    def __str__(self):
        return self.display_name or self.username

    def is_mod_or_admin(self):
        return self.role in ('moderator', 'admin')

    def is_admin_role(self):
        return self.role == 'admin'