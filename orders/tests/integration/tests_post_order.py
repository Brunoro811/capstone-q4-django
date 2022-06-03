from accounts.models import AccountModel
from accounts.tests.utils.util import user_admin_correct, user_seller_correct
from categories.models import CategoryModel
from orders.tests.utils import (
    fields_in_each_product_in_response,
    fields_in_products_in_response,
    fields_in_response,
    fields_in_variation_product,
    variation_creation_model,
    variation_request,
)
from products.models import ProductModel
from products.tests.utils.utils import correct_product
from rest_framework import status
from rest_framework.test import APITestCase
from stores.models import StoreModel
from stores.tests.utils import store_success
from variations.models import VariationModel


class TestPostOrder(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # criando admin
        cls.test_admin = AccountModel.objects.create_user(**user_admin_correct())
        # criando category
        test_category = CategoryModel.objects.create(name="test category")
        # criando store
        cls.test_store = StoreModel.objects.create(**store_success)
        test_product = ProductModel.objects.create(
            **correct_product(cls.test_store, test_category)
        )
        # criando seller
        cls.test_seller = AccountModel.objects.create_user(
            **user_seller_correct(), store_id=cls.test_store
        )
        # criando product
        variations = [
            VariationModel(**variation_creation_model(test_product)) for _ in range(8)
        ]
        # criando variations
        cls.variations_instances = VariationModel.objects.bulk_create(variations)

    def test_if_seller_can_create_order(self):
        self.client.force_authenticate(user=self.test_seller)
        response = self.client.post(
            "/orders/", variation_request(self.variations_instances), format="json"
        )

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for response_field in fields_in_response:
            # verifica se o campo está nos campos esperados ("id","created_at","total_value","seller_id","store_id","products")
            self.assertIn(response_field, response.json())
            if response_field == "products":
                # verifica os campos de cada produto, que é esperado ser uma lista
                for product in response.json()[response_field]:
                    # verifica se as chaves são as esperadas ("product", "sale_value", "quantity"), uso o set para ordenar alfabeticamente e não dar erro caso a ordem esteja trocada
                    self.assertEqual(
                        set(product.keys()),
                        set(fields_in_products_in_response),
                    )
                    # verifica se as chaves são as esperadas ( "id","name","cost_value","sale_value_retail","sale_value_wholesale","quantity_wholesale","store_id","category","variation",)
                    self.assertEqual(
                        set(product.get("product").keys()),
                        set(fields_in_each_product_in_response),
                    )
                    # verifica se as chaves são as esperadas ("id", "size", "color", "product_id")
                    self.assertEqual(
                        set(product.get("product").get("variation").keys()),
                        set(fields_in_variation_product),
                    )

    def test_if_user_cant_create_order_if_is_missing_some_field(self):
        self.client.force_authenticate(user=self.test_seller)
        response = self.client.post("/orders/", {}, format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("variations", response.json())
        self.assertEqual(response.json()["variations"], ["This field is required."])

    def test_if_user_cant_create_order_if_is_not_logged(self):
        response = self.client.post(
            "/orders/", variation_request(self.variations_instances), format="json"
        )

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.json())
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )

    def test_if_user_cant_create_order_if_is_not_a_seller(self):
        self.test_admin.is_seller = False
        self.test_admin.store_id = self.test_store
        self.test_admin.save()
        self.client.force_authenticate(user=self.test_admin)
        response = self.client.post(
            "/orders/", variation_request(self.variations_instances), format="json"
        )

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.json())
        self.assertEqual(
            response.json()["detail"],
            "You do not have permission to perform this action.",
        )
