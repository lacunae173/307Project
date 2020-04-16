from django.forms import ModelForm
from .models import Video

class VideoUploadForm(ModelForm):
    class Meta:
        model = Video
        fields = ['video', 'title', 'thumbnail', 'description']
        
        
