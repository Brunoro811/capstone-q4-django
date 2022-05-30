from accounts.models import AccountModel
from accounts.tests.utils import (fields_get_one_user, user_admin_correct,
                                  user_seller_correct)
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class TestAccounst(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_admin = AccountModel.objects.create_user(**user_admin_correct())
        cls.test_seller = AccountModel.objects.create_user(**user_seller_correct())

    def test_if_cant_get_one_user_without_authorization_header(self):
        user_id = str(self.test_admin.id)
        response = self.client.get(f"/accounts/{user_id}/", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.json())
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )

    def test_if_can_get_one_user_as_admin(self):
        user_id = str(self.test_admin.id)
        self.client.force_authenticate(user=self.test_admin)
        response = self.client.get(f"/accounts/{user_id}/", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field in fields_get_one_user:
            self.assertIn(field, response.json())

    def test_if_cant_get_one_user_as_seller(self):
        self.client.force_authenticate(user=self.test_seller)
        response = self.client.get(f"/accounts/{self.test_seller.id}/", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.json())
        self.assertEqual(
            response.json()["detail"],
            "You do not have permission to perform this action.",
        )

    def test_if_cant_get_one_user_if_user_dont_exists(self):
        self.client.force_authenticate(user=self.test_admin)
        response = self.client.get(
            "/accounts/230d81bf-2092-420a-a310-505ed9a1c243/", format="json"
        )
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.json())
        self.assertEqual(response.json()["detail"], "Not found.")
