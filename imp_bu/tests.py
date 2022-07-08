from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class ViewTests(APITestCase):
    url = reverse("api:bu-list")

    def test_impBu_get(self):
        response = self.client.head(self.url, secure=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_music_post(self):
    #     data = {"song": "Rick", "singer": "Rick"}
    #     response = self.client.post(self.url, data, secure=True)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_retrieve(self):
    #     response = self.client.get(reverse("MusicViewSet", kwargs={"pk": 1}))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
