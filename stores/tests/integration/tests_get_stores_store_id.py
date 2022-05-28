from accounts.models import AccountModel
from accounts.tests.utils.util import get_admin_payload, get_seller_payload
from rest_framework.test import APITestCase
from stores.models import StoreModel
from stores.tests.utils import (get_store_by_id_200_response_fields,
                                store_correct)


class TestStores(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.store_data = store_correct
        cls.store = StoreModel.objects.create(**cls.store_data)

        cls.seller_data = get_seller_payload()
        cls.seller = AccountModel.objects.create(**cls.seller_data)

        cls.admin_data = get_admin_payload()
        cls.admin = AccountModel.objects.create(**cls.admin_data)

    def test_if_cant_get_one_store_without_being_logged(self):
        response = self.client.get(f"/stores/{self.store.id}", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, 401)
        self.assertIn("detail", response.json())

    def test_if_can_get_one_store_as_admin(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(f"/stores/{self.store.id}", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, 200)

        for field in get_store_by_id_200_response_fields:
            self.assertIn(field, response.json())

    def test_if_cant_get_one_store_as_seller(self):
        self.client.force_authenticate(user=self.seller)

        response = self.client.get(f"/stores/{self.store.id}", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, 403)
        self.assertIn("detail", response.json())

    def test_if_cant_get_one_store_if_store_dont_exists(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(
            "/stores/230d81bf-2092-420a-a310-505ed9a1c243", format="json"
        )

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, 404)
        self.assertIn("detail", response.json())
