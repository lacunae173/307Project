from django.test import TestCase

from django.urls import reverse
from .models import *
from .views import *
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.
class TestVideo(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testUser',
            'password': 'password'
        }
        User.objects.create_user(**self.credentials)
        self.user = User.objects.get(username='testUser')
        self.client.force_login(self.user)
        dummy_video = SimpleUploadedFile("file.mp4", b"video", content_type="video/mp4")
        dummy_image = SimpleUploadedFile("file.png", b"image", content_type="image/png")
        self.video = Video.objects.create(owner=self.user, video=dummy_video, title="testvideo",thumbnail=dummy_image, description="testdescript")
    
    def test_watch_video(self):
        response = self.client.get(reverse('video', args=[self.video.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['video'].id, self.video.id)

    def test_watch_history(self):
        response = self.client.get(reverse('video', args=[self.video.id]))
        self.assertQuerysetEqual(History.objects.get_queryset(), [f'<History: uid:{self.user.id}-vid:{self.video.id}>'])

