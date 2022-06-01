from uuid import uuid4

from accounts.models import AccountModel
from accounts.tests.utils.util import get_admin_payload, get_seller_payload
from categories.models import CategoryModel
from categories.tests.utils import get_category_payload
from products.models import ProductModel
from rest_framework.status import (HTTP_200_OK, HTTP_401_UNAUTHORIZED,
                                   HTTP_404_NOT_FOUND)
from rest_framework.test import APITestCase
from stores.models import StoreModel
from stores.tests.utils.gen_store_functions import get_store_payload
from variations.models import VariationModel
from variations.tests.utils import list_variations_200_response_fields
from variations.tests.utils.gen_variation_functions import (
    get_product_payload, get_variation_payload)


class TestGetVariationById(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.seller_data = get_seller_payload()
        cls.seller: AccountModel = AccountModel.objects.create_user(**cls.seller_data)

        cls.admin_data = get_admin_payload()
        cls.admin: AccountModel = AccountModel.objects.create_user(**cls.admin_data)
        
        cls.category_data = get_category_payload()
        cls.category: CategoryModel = CategoryModel.objects.create(**cls.category_data)

        # Creating store
        cls.store_data = get_store_payload()
        cls.store: StoreModel = StoreModel.objects.create(**cls.store_data)

        cls.product_data = get_product_payload()
        cls.product: ProductModel = ProductModel.objects.create(
            **cls.product_data, category_id=cls.category, store_id=cls.store
        )

        cls.variation_data = get_variation_payload()
        cls.variation: VariationModel = VariationModel.objects.create(**cls.variation_data, product_id=cls.product)

    def test_if_user_cant_get_variation_by_id_without_being_logged(self):
        response = self.client.get(f"/products/variations/{self.variation.id}/", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.json())

    def test_if_admin_can_get_variation_by_id(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(f"/products/variations/{self.variation.id}/", format="json")
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, HTTP_200_OK)

        for field in list_variations_200_response_fields:
            self.assertIn(field, response.json())

    def test_if_seller_can_get_variation_by_id(self):
        self.client.force_authenticate(user=self.seller)

        response = self.client.get(f"/products/variations/{self.variation.id}/", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, HTTP_200_OK)

        for field in list_variations_200_response_fields:
            self.assertIn(field, response.json())
        
    def test_if_user_cant_get_variation_by_id_that_doesnt_exists(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(f"/products/variations/{uuid4()}/", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.json())

