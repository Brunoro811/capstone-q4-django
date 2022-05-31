from accounts.models import AccountModel
from accounts.tests.utils.util import user_admin_correct, user_seller_correct
from rest_framework import status
from rest_framework.test import APITestCase


class TestPostProduct(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_admin = AccountModel.objects.create_user(**user_admin_correct())
        cls.test_seller = AccountModel.objects.create_user(**user_seller_correct())

    def test_if_admin_can_get_all_products(self):
        self.client.force_authenticate(user=self.test_admin)
        response = self.client.get("/products/", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), list)

    def test_if_seller_can_get_all_products(self):
        self.client.force_authenticate(user=self.test_seller)
        response = self.client.get("/products/", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), list)

    def test_if_user_cant_get_all_products_if_is_not_logged(self):
        response = self.client.get("/products/", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.json())
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )
