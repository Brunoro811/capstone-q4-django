from uuid import uuid4

from accounts.models import AccountModel
from accounts.tests.utils.util import user_admin_correct, user_seller_correct
from categories.models import CategoryModel
from products.models import ProductModel
from products.tests.utils.utils import correct_product
from rest_framework import status
from rest_framework.test import APITestCase
from stores.models import StoreModel
from stores.tests.utils import store_success
from variations.models import VariationModel
from variations.tests.utils.patch_utils import (
    required_fields_in_response,
    variation_creation_model,
    variation_update_route,
)


class TestPostProduct(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_admin = AccountModel.objects.create_user(**user_admin_correct())
        cls.test_seller = AccountModel.objects.create_user(**user_seller_correct())
        test_category = CategoryModel.objects.create(name="test category")
        test_store = StoreModel.objects.create(**store_success)
        product = ProductModel.objects.create(
            **correct_product(test_store, test_category)
        )
        cls.test_product = product
        cls.test_variation = VariationModel.objects.create(
            **variation_creation_model(product)
        )

    def test_if_admin_can_update_a_product_variation(self):
        self.client.force_authenticate(user=self.test_admin)
        variation_id = self.test_variation.id
        response = self.client.patch(
            f"/products/variations/{variation_id}/",
            {**variation_update_route(str(self.test_product.id))},
            format="json",
        )

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field in required_fields_in_response:
            self.assertIn(field, response.json())

    def test_if_user_cant_update_a_product_variation_if_is_not_logged(self):
        variation_id = self.test_variation.id
        response = self.client.patch(
            f"/products/variations/{variation_id}/",
            {**variation_update_route(str(self.test_product.id))},
            format="json",
        )

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.json())
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )

    def test_if_seller_cant_update_product_variation(self):
        self.client.force_authenticate(user=self.test_seller)
        variation_id = self.test_variation.id
        response = self.client.patch(
            f"/products/variations/{variation_id}/",
            {**variation_update_route(str(self.test_product.id))},
            format="json",
        )

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.json())
        self.assertEqual(
            response.json()["detail"],
            "You do not have permission to perform this action.",
        )

    def test_if_user_cant_update_product_variation_if_it_doesnt_exists(self):
        self.client.force_authenticate(user=self.test_admin)
        variation_id = uuid4()
        response = self.client.patch(
            f"/products/variations/{variation_id}/",
            {**variation_update_route(str(self.test_product.id))},
            format="json",
        )

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.json())
        self.assertEqual(response.json()["detail"], "Not found.")

    def test_if_user_cant_update_a_product_variation_if_product_doesnt_exists(self):
        self.client.force_authenticate(user=self.test_admin)
        variation_id = self.test_variation.id

        response = self.client.patch(
            f"/products/variations/{variation_id}/",
            {**variation_update_route(uuid4())},
            format="json",
        )

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.json())
        self.assertEqual(response.json()["detail"], "Product not found.")
