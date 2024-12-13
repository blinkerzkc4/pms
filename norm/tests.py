from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from . import views


class NormsTests(APITestCase):
    def test_list_norms(self):
        url = reverse("norms-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class NormExtraCostTests(APITestCase):
    def test_list_norm_extra_costs(self):
        url = reverse("norm-costs-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class NormActivityTests(APITestCase):
    def test_list_norm_activity(self):
        url = reverse("norm-activity-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ActivityTypeTests(APITestCase):
    def test_list_activity_types(self):
        url = reverse("norm-activity-type-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class NormComponentsTests(APITestCase):
    def test_list_norm_components(self):
        url = reverse("norm-components-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
