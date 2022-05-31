from accounts.models import AccountModel
from accounts.tests.utils import get_admin_payload, get_seller_payload
from categorys.models import CategoryModel
from categorys.tests.utils import get_category_payload
from products.models import ProductModel
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from rest_framework.test import APITestCase
from stokar.utils.tests import forbidden_details, unauthorized_details
from stores.models import StoreModel
from stores.tests.utils import get_store_payload
from variations.models import VariationModel
from variations.tests.utils import (
    get_product_payload,
    get_variation_payload,
    list_variations_200_response_fields,
)


class TestGetVariation(APITestCase):
    PATH = "/products/variations/"

    @classmethod
    def setUpTestData(cls) -> None:
        # Creating seller
        cls.seller_data = get_seller_payload()
        cls.seller: AccountModel = AccountModel.objects.create_user(**cls.seller_data)

        # Creating admin
        cls.admin_data = get_admin_payload()
        cls.admin: AccountModel = AccountModel.objects.create_user(**cls.admin_data)

        # Creating category
        cls.category_data = get_category_payload()
        cls.category: CategoryModel = CategoryModel.objects.create(**cls.category_data)

        # Creating store
        cls.store_data = get_store_payload()
        cls.store: StoreModel = StoreModel.objects.create(**cls.store_data)

        # Creating product
        cls.product_data = get_product_payload()
        cls.product: ProductModel = ProductModel.objects.create(
            **cls.product_data, category_id=cls.category, store_id=cls.store
        )

    def test_if_admin_can_list_product_variations_200(self):
        # Inserting variations
        times = 5
        variations = [get_variation_payload(self.product.id) for _ in range(times)]
        VariationModel.objects.bulk_create(variations)

        # Authenticating with admin credentials
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(self.PATH, format="json")
        output = response.json()

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIsInstance(output, list)

        self.assertEqual(len(output), times)
        for variation in output:
            for field in list_variations_200_response_fields:
                # Testing if create response fields is returned
                self.assertIn(field, variation)

    def test_if_seller_can_list_product_variations_200(self):
        # Inserting variations
        times = 5
        variations = [get_variation_payload(self.product.id) for _ in range(times)]
        VariationModel.objects.bulk_create(variations)

        # Authenticating with admin credentials
        self.client.force_authenticate(user=self.seller)

        response = self.client.get(self.PATH, format="json")
        output = response.json()

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIsInstance(output, list)

        self.assertEqual(len(output), times)
        for variation in output:
            for field in list_variations_200_response_fields:
                # Testing if create response fields is returned
                self.assertIn(field, variation)

    def test_if_get_product_variations_evaluates_request_without_authorization_header_401(
        self,
    ):
        self.client.credentials(HTTP_AUTHORIZATION="")

        response = self.client.get(self.PATH, format="json")
        output = response.json()

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(output, unauthorized_details)
