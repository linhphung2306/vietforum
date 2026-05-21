from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Forum

@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display  = ['forum_name', 'topic_count', 'is_active', 'created_at']
    list_filter   = ['is_active']
    search_fields = ['forum_name']
    list_editable = ['is_active']