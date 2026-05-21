from django.urls import path
from . import views

app_name = 'moderation'

urlpatterns = [
    path('',                         views.dashboard,         name='dashboard'),
    path('report/<int:report_id>/',  views.handle_report,     name='handle_report'),
    path('topic/lock/<int:topic_id>/',views.toggle_lock_topic, name='lock_topic'),
    path('ban/<int:user_id>/',       views.ban_user,           name='ban_user'),
    path('users/', views.user_list, name='user_list'),
    path('reports/', views.report_dashboard, name='report_dashboard'),
]