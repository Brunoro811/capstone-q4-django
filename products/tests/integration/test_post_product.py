from accounts.models import AccountModel
from accounts.tests.utils.util import user_admin_correct, user_seller_correct
from products.tests.utils.utils import correct_product_route, products_fields_response
from rest_framework import status
from rest_framework.test import APITestCase
from stores.models import StoreModel
from stores.tests.utils import store_success


class TestPostProduct(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_admin = AccountModel.objects.create_user(**user_admin_correct())
        cls.test_seller = AccountModel.objects.create_user(**user_seller_correct())
        test_store = StoreModel.objects.create(**store_success)
        cls.correct_product = correct_product_route(
            str(test_store.id), "categoria teste"
        )

    def test_if_admin_can_create_a_product(self):
        self.client.force_authenticate(user=self.test_admin)
        response = self.client.post("/products/", self.correct_product, format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for item in products_fields_response:
            self.assertIn(item, response.json())
            self.assertEqual(response.json()[item], correct_product_route()[item])

    def test_if_seller_can_create_a_product(self):
        self.client.force_authenticate(user=self.test_seller)
        response = self.client.post("/products/", self.correct_product, format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for item in products_fields_response:
            self.assertIn(item, response.json())
            self.assertEqual(response.json()[item], correct_product_route()[item])

    def test_if_user_cant_create_a_product_missing_fields(self):
        self.client.force_authenticate(user=self.test_admin)
        for item in correct_product_route():
            
            response = self.client.post(
                "/products/", self.correct_product, format="json"
            )

            self.assertEqual(response.headers["Content-Type"], "application/json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
