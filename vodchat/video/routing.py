from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    path('ws/video/<int:video_id>/', consumers.VideoConsumer, name='videoChat'), ##!!!!!!!!!!!!!!!
]


