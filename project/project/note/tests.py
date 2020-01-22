from django.test import TestCase
from django.urls import reverse
from .models import Note, Label
# Create your tests here.
BASE_URL = 'http://127.0.0.1:8000/note/'


class NoteTest(TestCase):
    fixtures = ['test_db']

    def test_note_get(self):
        url = BASE_URL + reverse('list-note')
        resp = self.client.get(url, content_type='application/json')
        self.assertEqual(resp.status_code, 200)
