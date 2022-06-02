from accounts.models import AccountModel
from accounts.tests.utils.util import user_admin_correct, user_seller_correct
from categories.models import CategoryModel
from orders.models import OrderModel
from orders.tests.utils import (
    fields_in_each_product_in_response,
    fields_in_products_in_response,
    fields_in_response,
    fields_in_variation_product,
    variation_creation_model,
)
from products.models import ProductModel
from products.tests.utils.utils import correct_product
from rest_framework import status
from rest_framework.test import APITestCase
from stores.models import StoreModel
from stores.tests.utils import store_success
from variations.models import VariationModel


class TestGetOrder(APITestCase):
    @classmethod
    def setUpTestData(cls):
        test_category = CategoryModel.objects.create(name="test category")
        test_store = StoreModel.objects.create(**store_success)
        test_admin = AccountModel.objects.create_user(
            **user_admin_correct(), store_id=test_store
        )
        test_seller = AccountModel.objects.create_user(
            **user_seller_correct(), store_id=test_store
        )
        cls.test_admin = test_admin
        cls.test_seller = test_seller
        test_product = ProductModel.objects.create(
            **correct_product(test_store, test_category)
        )
        variations = [
            VariationModel(**variation_creation_model(test_product)) for _ in range(8)
        ]
        VariationModel.objects.bulk_create(variations)
        cls.variations_instances = VariationModel.objects.all()
        OrderModel.objects.create()

    def test_if_seller_can_get_its_order(self):
        self.client.force_authenticate(user=self.test_seller)
        response = self.client.get("/orders/", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), list)
        for order in response.json():
            self.assertEqual(order.seller_id, self.test_seller)
            for response_field in fields_in_response:
                self.assertIn(response_field, response.json())
                if response_field == "products":
                    for product in response.json()[response_field]:
                        self.assertEqual(
                            set(product.keys()),
                            set(fields_in_products_in_response),
                        )
                        self.assertEqual(
                            set(product.get("product").keys()),
                            set(fields_in_each_product_in_response),
                        )
                        self.assertEqual(
                            set(product.get("product").get("variant").keys()),
                            set(fields_in_variation_product),
                        )

    def test_if_admin_can_get_all_orders(self):
        self.client.force_authenticate(user=self.test_admin)
        response = self.client.get("/orders/", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
