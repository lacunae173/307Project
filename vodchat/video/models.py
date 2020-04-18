from django.db import models
from django.contrib.auth.models import User

def get_video_upload_path(instance, filename):
    return 'user-' + str(instance.owner.id) + '/video/' + filename

def get_thumbnail_upload_path(instance, filename):
  return 'user-' + str(instance.owner.id) + '/thumbnail/' + filename

# Create your models here.
class Video(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.FileField(upload_to=get_video_upload_path)
    title = models.CharField(max_length=100)
    thumbnail = models.FileField(upload_to=get_thumbnail_upload_path)
    description = models.CharField(max_length=10000)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
       ordering = ['-created']

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    time_watched = models.DateTimeField(auto_now_add=True) 
    class Meta:
       ordering = ['-time_watched']  