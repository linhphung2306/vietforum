from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Topic, Post

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display  = ['title', 'forum', 'author', 'view_count',
                     'is_pinned', 'is_locked', 'created_at']
    list_filter   = ['forum', 'is_pinned', 'is_locked']
    search_fields = ['title', 'author__username']
    list_editable = ['is_pinned', 'is_locked']
    actions       = ['pin_topics', 'unpin_topics', 'lock_topics', 'unlock_topics']

    def pin_topics(self, request, qs):
        qs.update(is_pinned=True)
    pin_topics.short_description = 'Ghim các chủ đề đã chọn'

    def lock_topics(self, request, qs):
        qs.update(is_locked=True)
    lock_topics.short_description = 'Khóa các chủ đề đã chọn'

    def unpin_topics(self, request, qs):
        qs.update(is_pinned=False)
    def unlock_topics(self, request, qs):
        qs.update(is_locked=False)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display  = ['id', 'topic', 'author', 'is_deleted', 'created_at']
    list_filter   = ['is_deleted']
    search_fields = ['content', 'author__username']