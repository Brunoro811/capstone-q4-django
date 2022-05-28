from uuid import uuid4

from accounts.models import AccountModel
from accounts.tests.utils import user_admin_correct as function_user_admin_correct
from accounts.tests.utils import user_seller_correct as function_user_seller_correct
from rest_framework import status
from rest_framework.test import APITestCase
from stores.models import StoreModel
from stores.tests.utils import store_correct


class TestStore(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user_admin_correct = function_user_admin_correct()
        user_seller_correct = function_user_seller_correct()
        cls.test_admin = AccountModel.objects.create_user(**user_admin_correct)
        cls.test_seller = AccountModel.objects.create_user(**user_seller_correct)
        cls.test_store = StoreModel.objects.create(**store_correct)

    def test_if_store_can_be_activated_logged_as_admin(self):
        self.client.force_authenticate(user=self.test_admin)
        self.test_store.is_active=False
        self.test_store.save()
        response = self.client.patch(
            f"/stores/activate/{self.test_store.id}/", format="json"
        )

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("detail", response.json())
        self.assertEqual(
            response.json()["detail"], f"store {self.test_store.name} activated"
        )

    def test_if_store_cant_be_activated_without_authorization_headers(self):
        response = self.client.patch(
            f"/stores/activate/{self.test_store.id}/", format="json"
        )

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.json())
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )

    def test_if_store_cant_be_activated_logged_as_seller(self):
        self.client.force_authenticate(user=self.test_seller)
        response = self.client.patch(
            f"/stores/activate/{self.test_store.id}/", format="json"
        )

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.json())
        self.assertEqual(
            response.json()["detail"],
            "You do not have permission to perform this action.",
        )

    def test_if_store_cant_be_activated_if_it_doesnt_exists(self):
        self.client.force_authenticate(user=self.test_admin)
        response = self.client.patch(f"/stores/activate/{uuid4()}/", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.json())
        self.assertEqual(response.json()["detail"], "Not found.")

    def test_if_store_cant_be_activated_if_it_is_already_active(self):
        self.client.force_authenticate(user=self.test_admin)
        self.client.patch(f"/stores/activate/{self.test_store.id}/", format="json")
        response = self.client.patch(
            f"/stores/activate/{self.test_store.id}/", format="json"
        )

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertIn("detail", response.json())
        self.assertEqual(
            response.json()["detail"], "store with this id is already active"
        )
