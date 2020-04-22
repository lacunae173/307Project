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

    def __str__(self):
        return f'{self.id}-{self.title}-by:{self.owner.id}'

    class Meta:
       ordering = ['-created']

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    time_watched = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
      return f'uid:{self.user.id}-vid:{self.video.id}'

    class Meta:
       ordering = ['-time_watched']  

class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    text = models.CharField(max_length=10000)
    time = models.FloatField() 
    vote = models.IntegerField() 
    def __str__(self):
        return f'cid:{self.id}-vid:{self.video.id}'
