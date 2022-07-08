from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class ViewTests(APITestCase):
    url = reverse("api:extnames-list")
    # url_div = reverse("api:div-list")
    # url_extnames_query_name_div = reverse("api:extnames/query_name_div")

    def test_impExtnames_get(self):
        response = self.client.head(self.url, secure=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_query_name_div(self):
    #     data_div = {
    #         "div": "MLT",
    #         "function": "test",
    #         "div_code": "MLTest",
    #         "rate": 100000,
    #     }
    #     response_div = self.client.post(self.url, data_div, secure=True)
    #     self.assertEqual(response_div.status_code, status.HTTP_201_CREATED)
    # data = {
    #     "emp_name": "hank",
    #     "div": "ll",
    # }
    # response = self.client.post(self.url, data, secure=True)
    # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
