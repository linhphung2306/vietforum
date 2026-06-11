from django.urls import path
from . import views

app_name = 'interactions'

urlpatterns = [
    path('vote/<int:post_id>/',                      views.vote,              name='vote'),
    path('report/<int:post_id>/',                    views.report,            name='report'),
]