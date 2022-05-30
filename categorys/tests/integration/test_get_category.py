from uuid import uuid4

from accounts.models import AccountModel
from accounts.tests.utils.util import get_admin_payload, get_seller_payload
from rest_framework import status
from rest_framework.test import APITestCase


class TestCategories(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = AccountModel.objects.create_user(**get_admin_payload())
        cls.seller = AccountModel.objects.create_user(**get_seller_payload())

    def test_if_user_cant_get_categories_without_authorization_header(self):
        response = self.client.get("/categories/", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.json())

    def test_if_admin_can_get_categories(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/categories/", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.json())
        self.assertIn("name", response.json())
        self.assertIsInstance(response.json()["name"], str)

    def test_if_seller_can_get_categories(self):
        self.client.force_authenticate(user=self.seller)
        response = self.client.get("/categories/", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.json())
        self.assertIn("name", response.json())
        self.assertIsInstance(response.json()["name"], str)

