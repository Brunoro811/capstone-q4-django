from accounts.models import AccountModel
from accounts.tests.utils import get_admin_payload, get_seller_payload
from categorys.models import CategoryModel
from categorys.tests.utils import get_category_payload
from products.models import ProductModel
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
)
from rest_framework.test import APITestCase
from stokar.utils.tests import forbidden_details, unauthorized_details
from stores.models import StoreModel
from stores.tests.utils import get_store_payload
from variations.tests.utils import (
    create_variation_201_response_fields,
    get_post_variation_payload,
    get_product_payload,
    get_variation_payload,
)


class TestPostVariation(APITestCase):
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

    def test_if_creates_product_variation_201(self):
        # Authenticating with admin credentials
        self.client.force_authenticate(user=self.admin)

        data = get_post_variation_payload(self.product.id)

        # Checking individualy if the updatable fields may be updated

        response = self.client.post(self.PATH, data, format="json")
        output = response.json()

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        for field in create_variation_201_response_fields:
            # Testing if create response fields is returned
            self.assertIn(field, output)

    def test_if_post_product_variations_evaluates_wrong_schema_400(self):

        # Authenticating with admin credentials
        self.client.force_authenticate(user=self.admin)

        data = get_post_variation_payload(self.product.id)

        # Popping one field and testing if returns correct message
        for field in data.keys():
            payload = {**data}
            payload.pop(field)

            response = self.client.post(self.PATH, payload, format="json")
            output = response.json()

            self.assertEqual(response.headers["Content-Type"], "application/json")
            self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

            error_message = {field: ["This field is required."]}

            self.assertEqual(output, error_message)

    def test_if_post_product_variations_evaluates_request_without_authorization_header_401(
        self,
    ):

        self.client.credentials(HTTP_AUTHORIZATION="")

        data = get_post_variation_payload(self.product.id)

        response = self.client.post(self.PATH, data, format="json")
        output = response.json()

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(output, unauthorized_details)

    def test_if_seller_can_not_create_category_403(self):

        # Authenticating with seller credentials
        self.client.force_authenticate(user=self.seller)

        data = get_post_variation_payload(self.product.id)

        response = self.client.post(self.PATH, data, format="json")
        output = response.json()

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(output, forbidden_details)
