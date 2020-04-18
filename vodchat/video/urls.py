from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("<int:video_id>", video, name="video"),
    path('videos', videos, name='videos'),
    path('my_page', my_page, name='my_page'),
    path('delete_upload', delete_upload, name='delete_upload'),
]
