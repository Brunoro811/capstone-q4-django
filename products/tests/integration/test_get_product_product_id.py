from uuid import uuid4

from accounts.models import AccountModel
from accounts.tests.utils.util import user_admin_correct, user_seller_correct
from categorys.models import CategoryModel
from products.models import ProductModel
from products.tests.utils.utils import correct_product
from rest_framework import status
from rest_framework.test import APITestCase
from stores.models import StoreModel
from stores.tests.utils import store_success


class TestGetProduct(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_admin = AccountModel.objects.create_user(**user_admin_correct())
        cls.test_seller = AccountModel.objects.create_user(**user_seller_correct())
        test_category = CategoryModel.objects.create(name="test category")
        test_store = StoreModel.objects.create(**store_success)
        cls.test_product = ProductModel.objects.create(
            **correct_product(test_store, test_category)
        )

    def test_if_admin_can_get_a_product(self):
        product_id = self.test_product.id
        self.client.force_authenticate(user=self.test_admin)
        response = self.client.get(f"/products/{product_id}/", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.json())
        self.assertEqual(response.json()["id"], str(product_id))
        self.assertIn("name", response.json())
        self.assertIsInstance(response.json()["name"], str)

    def test_if_seller_can_get_a_product(self):
        product_id = self.test_product.id
        self.client.force_authenticate(user=self.test_seller)
        response = self.client.get(f"/products/{product_id}/", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.json())
        self.assertEqual(response.json()["id"], str(product_id))
        self.assertIn("name", response.json())
        self.assertIsInstance(response.json()["name"], str)

    def test_if_user_cant_get_product_without_authorization_header(self):
        product_id = self.test_product.id
        response = self.client.get(f"/products/{product_id}/", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.json())
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )

    def test_if_user_cant_get_a_product_that_doesnt_exists(self):
        product_id = uuid4()
        self.client.force_authenticate(user=self.test_admin)
        response = self.client.get(f"/products/{product_id}/", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.json())
        self.assertEqual(response.json()["detail"], "Not found.")
