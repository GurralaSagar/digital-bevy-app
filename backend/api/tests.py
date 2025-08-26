from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

class RepoApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_search_requires_keyword(self):
        resp = self.client.post(reverse('search_and_store'), {})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
