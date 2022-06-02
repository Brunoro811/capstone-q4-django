from accounts.models import AccountModel
from accounts.tests.utils.util import user_admin_correct, user_seller_correct
from categories.models import CategoryModel
from orders.models import OrdersModel, OrderVariationsModel
from orders.tests.utils import (
    fields_in_each_product_in_response,
    fields_in_products_in_response,
    fields_in_response,
    fields_in_variation_product,
    order_and_order_variations,
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

        # criando category
        test_category = CategoryModel.objects.create(name="test category")

        # criando store
        test_store = StoreModel.objects.create(**store_success)

        # criando admin
        test_admin = AccountModel.objects.create_user(
            **user_admin_correct(), store_id=test_store
        )

        # criando seller
        test_seller = AccountModel.objects.create_user(
            **user_seller_correct(), store_id=test_store
        )

        # criando product
        test_product = ProductModel.objects.create(
            **correct_product(test_store, test_category)
        )

        # criando variations
        test_variations = VariationModel.objects.bulk_create(
            [VariationModel(**variation_creation_model(test_product)) for _ in range(8)]
        )

        # criando order e order variations do seller
        (seller_order, seller_order_variations,) = order_and_order_variations(
            test_variations, str(test_seller.id), str(test_store.id)
        )

        # criando order e order variations do admin
        (admin_order, admin_order_variations,) = order_and_order_variations(
            test_variations, str(test_admin.id), str(test_store.id)
        )
        cls.test_category = test_category
        cls.test_store = test_store
        cls.test_admin = test_admin
        cls.test_seller = test_seller
        cls.test_product = test_product
        cls.test_variations = test_variations
        cls.seller_order = seller_order
        cls.seller_order_variations = seller_order_variations
        cls.admin_order = admin_order
        cls.admin_order_variations = admin_order_variations

    def test_if_seller_can_get_its_order(self):
        self.client.force_authenticate(user=self.test_seller)
        response = self.client.get("/orders/", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), list)
        self.assertTrue(len(response.json()) <= len(OrderVariationsModel.objects.all()))
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

    def test_if_admin_can_get_all_order(self):
        self.client.force_authenticate(user=self.test_seller)
        response = self.client.get("/orders/", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), list)
        self.assertTrue(len(response.json()) == len(OrdersModel.objects.all()))
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
