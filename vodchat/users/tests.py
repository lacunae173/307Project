from django.test import TestCase

from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.
class TestLogIn(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testUser',
            'password': 'password'
        }
        User.objects.create_user(**self.credentials)
    
    def test_login(self):
        response = self.client.post(reverse('login'), self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)
