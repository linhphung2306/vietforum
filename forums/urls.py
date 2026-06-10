from django.urls import path
from . import views

app_name = 'forums'

urlpatterns = [
    path('', views.home, name='home'),
    path('forum/create/', views.create_forum, name='create_forum'),
    path('forum/<int:forum_id>/delete/', views.delete_forum, name='delete_forum'),
    path('forum/<int:forum_id>/approve/', views.approve_forum, name='approve_forum'),
    path('forum/pending/', views.pending_forums, name='pending_forums'),
]