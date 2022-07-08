from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class ViewTests(APITestCase):
    url = reverse("api:div-list")

    def test_impDiv_get(self):
        response = self.client.head(self.url, secure=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)