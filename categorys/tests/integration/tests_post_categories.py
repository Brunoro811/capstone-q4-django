from uuid import uuid4

from accounts.models import AccountModel
from accounts.tests.utils import get_admin_payload, get_seller_payload
from categorys.models import CategoryModel
from categorys.tests.utils import (
    create_category_200_response_fields,
    forbidden_details,
    get_category_payload,
    store_name_conflict_details,
    unauthorized_details,
)
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_409_CONFLICT,
)
from rest_framework.test import APITestCase


class TestStorePATCH(APITestCase):
    PATH = "/categories/"

    @classmethod
    def setUpTestData(cls) -> None:
        # Creating seller
        cls.seller_data = get_seller_payload()
        cls.seller: AccountModel = AccountModel.objects.create(**cls.seller_data)

        # Creating admin
        cls.admin_data = get_admin_payload()
        cls.admin: AccountModel = AccountModel.objects.create(**cls.admin_data)

        # Creating category
        cls.category_data = get_category_payload()
        cls.store: CategoryModel = CategoryModel.objects.create(**cls.category_data)

    def test_if_creates_category_201(self):
        # Authenticating with admin credentials
        self.client.force_authenticate(user=self.admin)

        data = get_category_payload()

        # Checking individualy if the updatable fields may be updated

        response = self.client.post(self.PATH, data, format="json")

        output = response.json()

        for field, value in data.items():
            self.assertEqual(response.headers["Content-Type"], "application/json")
            self.assertEqual(response.status_code, HTTP_201_CREATED)

            # Testing if updated field is returned
            self.assertIn(field, output)
            self.assertEqual(output[field].lower(), value.lower())

        # Testing if response payload has only correct fields
        self.assertEqual(set(output), set(create_category_200_response_fields))

    def test_if_post_categories_evaluates_wrong_schema_400(self):

        # Authenticating with admin credentials
        self.client.force_authenticate(user=self.admin)

        data = get_category_payload()

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

    def test_if_post_categories_evaluates_request_without_authorization_header_401(
        self,
    ):

        self.client.credentials(HTTP_AUTHORIZATION="")

        data = get_category_payload()

        response = self.client.post(self.PATH, data, format="json")
        output = response.json()

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(output, unauthorized_details)

    def test_if_seller_can_not_create_category_403(self):

        # Authenticating with seller credentials
        self.client.force_authenticate(user=self.seller)

        data = get_category_payload()

        response = self.client.post(self.PATH, data, format="json")
        output = response.json()

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(output, forbidden_details)

    def test_if_evaluates_category_name_unicity_409(self):

        # Authenticating with admin credentials
        self.client.force_authenticate(user=self.admin)

        # Creating new store
        new_category: CategoryModel = CategoryModel.objects.create(
            **get_category_payload()
        )

        # Repeating `name` to force unicity error
        data = {"name": new_category.name}

        response = self.client.post(self.PATH, data, format="json")
        output = response.json()

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, HTTP_409_CONFLICT)
        self.assertEqual(output, store_name_conflict_details)
