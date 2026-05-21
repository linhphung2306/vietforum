from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Vote, Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display  = ['id', 'post', 'reporter', 'status',
                     'reviewed_by', 'created_at', 'resolved_at']
    list_filter   = ['status']
    list_editable = ['status']