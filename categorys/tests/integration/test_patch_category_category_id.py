from uuid import uuid4

from accounts.models import AccountModel
from accounts.tests.utils.util import user_admin_correct, user_seller_correct
from categorys.models import CategoryModel
from rest_framework import status
from rest_framework.test import APITestCase


class TestGetCategory(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_admin = AccountModel.objects.create_user(**user_admin_correct())
        cls.test_seller = AccountModel.objects.create_user(**user_seller_correct())
        cls.test_category = CategoryModel.objects.create(name="test category")

    def test_if_admin_can_update_a_category(self):
        category_id = self.test_category.id
        self.client.force_authenticate(user=self.test_admin)
        response = self.client.patch(
            f"/categories/{category_id}/", {"name": "test category 2"}, format="json"
        )

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.json())
        self.assertEqual(response.json()["id"], str(category_id))
        self.assertIn("name", response.json())
        self.assertIsInstance(response.json()["name"], str)

    def test_if_user_cant_update_a_category_without_authorization_header(self):
        category_id = self.test_category.id
        response = self.client.patch(
            f"/categories/{category_id}/", {"name": "test category 3"}, format="json"
        )

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.json())
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )

    def test_if_seller_cant_update_a_category(self):
        category_id = self.test_category.id
        self.client.force_authenticate(user=self.test_seller)
        response = self.client.patch(
            f"/categories/{category_id}/", {"name": "test category 4"}, format="json"
        )

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.json())
        self.assertEqual(
            response.json()["detail"],
            "You do not have permission to perform this action.",
        )

    def test_if_user_cant_update_a_category_that_doesnt_exists(self):
        category_id = uuid4()
        self.client.force_authenticate(user=self.test_admin)
        response = self.client.get(f"/categories/{category_id}/", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.json())
        self.assertEqual(response.json()["detail"], "Not found.")
