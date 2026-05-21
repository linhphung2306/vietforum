from django.urls import path
from . import views

app_name = 'forums'

urlpatterns = [
    path('forum/create/', views.create_forum, name='create_forum'),
]