from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display  = ['username', 'email', 'display_name', 'role', 'is_active']
    list_filter   = ['role', 'is_active']
    list_editable = ['role', 'is_active']
    fieldsets     = UserAdmin.fieldsets + (
        ('Thông tin thêm', {
            'fields': ('display_name', 'avatar_url', 'role', 'bio')
        }),
    )