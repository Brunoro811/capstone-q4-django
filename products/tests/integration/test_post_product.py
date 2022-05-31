import random

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
            self.assertEqual(response.json()[item], self.correct_product[item])

    def test_if_user_cant_create_a_product_missing_fields(self):
        self.client.force_authenticate(user=self.test_admin)
        missin_field = list(self.correct_product.keys()).pop(
            random.randint(0, len(self.correct_product.keys()) - 1)
        )
        correct_product_clone = {**self.correct_product}
        correct_product_clone.pop(missin_field)
        response = self.client.post("/products/", correct_product_clone, format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(missin_field, response.json())
        self.assertEqual(response.json()[missin_field], ["This field is required."])
        
    def test_if_user_can_create_a_product_withou_beeing_logged(self):
        response = self.client.post('/products/', self.correct_product, format='json')
        
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.json())
        self.assertEqual(response.json()['detail'], 'Authentication credentials were not provided.')
        
    def test_if_seller_cant_create_a_product(self):
        self.client.force_authenticate(user=self.test_seller)
        response = self.client.post("/products/", self.correct_product, format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.json())
        self.assertEqual(
            response.json()["detail"],
            "You do not have permission to perform this action.",
        )
