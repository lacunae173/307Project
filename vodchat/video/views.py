from django.shortcuts import render
from .models import Video
from .forms import VideoUploadForm
from django.contrib.auth.decorators import login_required
from users.views import index

# Create your views here.


def videos(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    context = {'videos': Video.objects.all()}
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.owner = request.user
            inst.save()
        context['form'] = form
    return render(request, 'video/videos.html', context)

def video(request, video_id):
    try:
        video = Video.objects.get(pk=video_id)
    except Flight.DoesNotExist:
        raise Http404("Video does not exist")
    context = {
        "video": video
    }
    return render(request, "video/video.html", context)
