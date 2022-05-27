import random

from accounts.models import AccountModel
from accounts.tests.utils import user_admin_correct as function_user_admin_correct
from accounts.tests.utils import user_seller_correct as function_user_seller_correct
from rest_framework import status
from rest_framework.test import APITestCase
from stores.tests.utils import (
    fields_request_create_store,
    fields_response_create_store,
    store_success,
)


class TestStore(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user_admin_correct = function_user_admin_correct()
        user_seller_correct = function_user_seller_correct()
        cls.test_admin = AccountModel.objects.create_user(**user_admin_correct)
        cls.test_seller = AccountModel.objects.create_user(**user_seller_correct)

    def test_if_admin_can_create_store(self):
        self.client.force_authenticate(user=self.test_admin)
        response = self.client.post("/stores/", store_success, format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for field in response.json().keys():
            self.assertIn(field, fields_response_create_store)
        self.assertTrue(response.json()["is_active"])

    def test_if_store_cant_be_created_without_authentication_headers(self):
        response = self.client.post("/stores/", store_success, format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.json())
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )

    def test_if_seller_cant_create_store(self):
        self.client.force_authenticate(user=self.test_seller)
        response = self.client.post("/stores/", store_success, format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.json())
        self.assertEqual(
            response.json()["detail"],
            "You do not have permission to perform this action.",
        )

    def test_if_store_cant_be_created_with_an_existing_name(self):
        self.client.force_authenticate(user=self.test_admin)
        self.client.post("/stores/", store_success, format="json")
        response = self.client.post("/stores/", store_success, format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertIn("name", response.json())
        self.assertEqual(
            response.json()["name"], ["store with this name already exists."]
        )

    def test_if_admin_cant_create_store_with_missing_fields(self):
        self.client.force_authenticate(user=self.test_admin)
        missing_field = fields_request_create_store.pop(
            random.randint(0, len(fields_request_create_store) - 1)
        )
        store_success_clone = {**store_success}
        store_success_clone.pop(missing_field)
        response = self.client.post("/stores/", store_success_clone, format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(missing_field, response.json())
        self.assertEqual(response.json()[missing_field], ["This field is required."])
