from django.shortcuts import render
from .models import Video, History
from .forms import VideoUploadForm
from django.contrib.auth.decorators import login_required
from users.views import index
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, QueryDict
import json
# Create your views here.


def videos(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    context = {'videos': Video.objects.all()}
    
    return render(request, 'video/videos.html', context)

def video(request, video_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    try:
        
        video = Video.objects.get(pk=video_id)
        history = History(user=request.user, video=video)
        history.save()
        request.user.history_set.add(history)
    except Video.DoesNotExist:
        raise Http404("Video does not exist")
    context = {
        "video": video
    }
    return render(request, "video/video.html", context)

def my_page(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    username = request.user.username
    uploads = request.user.video_set.all()
    history = request.user.history_set.all()
    context = {
        "username": username,
        "uploads": uploads,
        "history": history,
    }
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.owner = request.user
            inst.save()
            context['form'] = form
    return render(request, 'video/my_page.html', context)

def delete_upload(request):
    if request.method == 'POST':
        video = Video.objects.get(pk=int(QueryDict(request.body).get('video_pk')))
        video.delete()

        response_data = {}
        response_data['msg'] = 'Post was deleted.'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "nothing to see"}),
            content_type="application/json"
        )