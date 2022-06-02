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
        cls.test_admin = AccountModel.objects.create_user(**user_admin_correct())
        cls.test_seller = AccountModel.objects.create_user(**user_seller_correct())
        test_category = CategoryModel.objects.create(name="test category")
        test_store = StoreModel.objects.create(**store_success)
        test_product = ProductModel.objects.create(
            **correct_product(test_store, test_category)
        )
        variations = [
            VariationModel(**variation_creation_model(test_product)) for _ in range(8)
        ]
        VariationModel.objects.bulk_create(variations)
        cls.variations_instances = VariationModel.objects.all()

    def test_if_seller_can_create_order(self):
        self.client.force_authenticate(user=self.test_seller)
        response = self.client.post(
            "/orders/", variation_request(self.variations_instances), format="json"
        )

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # verifica cada campo do response.json(), que é esperado ser um objeto(
        # {
        # 	"id": uuid,
        # 	"created_at": datetime,
        # 	"total_value": float,
        # 	"seller_id": uuid (do seller que fez a requisição),
        # 	"store_id": uuid,
        # 	"products":[
        # 		{
        # 			"product": {
        # 				"id": uuid,
        # 				"name": string,
        # 			  "cost_value": float,
        # 				"sale_value_retail": float,
        # 				"sale_value_wholesale": float,
        # 				"quantity_wholesale": integer,
        # 				"store_id": uuid,
        # 				"category": string,
        # 				"variation": {
        # 					"id": uuid,
        # 					"size": string,
        # 					"color": string,
        # 					"product_id": uuid,
        # 					}
        # 				},
        # 			"sale_value": float,
        # 			"quantity": int,
        # 		},
        # 		(...)
        # 	]
        # })
        for response_field in fields_in_response:
            # verifica se o campo está nos campos esperados
            self.assertIn(response_field, response.json())
            if response_field == "products":
                # verifica os campos de cada produto, que é esperado ser uma lista
                for product in response.json()[response_field]:
                    # verifica se as chaves são as esperadas
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

    def test_if_user_cant_create_order_if_is_missing_some_field(self):
        self.client.force_authenticate(user=self.test_seller)
        response = self.client.post("/orders/", {}, format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("variations", response.json())
        self.assertEqual(response.json()["variations"], ["This field is required"])

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
