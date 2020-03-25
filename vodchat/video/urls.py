from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("<int:video_id>", video, name="video"),
    path('videos', videos, name='videos')
]
