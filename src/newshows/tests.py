from django.test import SimpleTestCase, TestCase
from django.http import HttpRequest
from django.urls import reverse

from . import views


class StatusCodeTests(TestCase):
    
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_shows_page_status_code(self):
        response = self.client.get('/shows')
        self.assertEquals(response.status_code, 301)

    def test_settings_page_status_code(self):
        response = self.client.get('/settings')
        self.assertEquals(response.status_code, 301)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('settings'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings.html')

