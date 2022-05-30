from uuid import uuid4

from accounts.models import AccountModel
from accounts.tests.utils.util import user_admin_correct, user_seller_correct
from categorys.models import CategoryModel
from products.models import ProductModel
from products.tests.utils.utils import (
    correct_product,
    product_update,
    products_fields_response,
)
from rest_framework import status
from rest_framework.test import APITestCase
from stores.models import StoreModel
from stores.tests.utils import store_success, store_success_update


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
        test_another_store = StoreModel.objects.create(**store_success_update)
        test_another_category = CategoryModel.objects.create(
            name="another test category"
        )
        cls.product_update = product_update(test_another_store, test_another_category)

    def test_if_admin_can_update_a_product(self):
        product_id = self.test_product.id
        self.client.force_authenticate(user=self.test_admin)
        for key, value in self.product_update.items():
            if key != "store_id" and key != "category_id":
                response = self.client.patch(
                    f"/products/{product_id}/", {key: value}, format="json"
                )

                self.assertEqual(response.headers["Content-Type"], "application/json")
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                for product_field in products_fields_response:
                    if product_field == key:
                        self.assertIn(product_field, response.json())
                        self.assertEqual(response.json()[product_field], value)
            else:
                if key == "store_id":
                    response = self.client.patch(
                        f"/products/{product_id}/", {key: value}, format="json"
                    )

    def test_if_user_cant_update_a_product_without_authorization_header(self):
        product_id = self.test_product.id
        response = self.client.patch(
            f"/products/{product_id}/", {"name": "test product 3"}, format="json"
        )

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.json())
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )

    def test_if_seller_cant_update_a_product(self):
        product_id = self.test_product.id
        self.client.force_authenticate(user=self.test_seller)
        response = self.client.patch(
            f"/products/{product_id}/", {"name": "test product 4"}, format="json"
        )

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.json())
        self.assertEqual(
            response.json()["detail"],
            "You do not have permission to perform this action.",
        )

    def test_if_user_cant_update_a_product_that_doesnt_exists(self):
        product_id = uuid4()
        self.client.force_authenticate(user=self.test_admin)
        response = self.client.get(f"/products/{product_id}/", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.json())
        self.assertEqual(response.json()["detail"], "Not found.")
