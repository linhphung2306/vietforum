from django.urls import path
from . import views

app_name = 'topics'

urlpatterns = [
    path('forum/<int:forum_id>/',      views.forum_detail,  name='forum_detail'),
    path('topic/<int:topic_id>/',      views.topic_detail,  name='topic_detail'),
    path('topic/create/<int:forum_id>/',views.create_topic,  name='create_topic'),
    path('topic/edit/<int:topic_id>/',  views.edit_topic,    name='edit_topic'),
    path('post/delete/<int:post_id>/',  views.delete_post,   name='delete_post'),
    path('search/', views.search, name='search'),
    path('topic/pin/<int:topic_id>/', views.pin_topic, name='pin_topic'),
    path('post/edit/<int:post_id>/', views.edit_post, name='edit_post'),
]