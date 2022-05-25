from accounts.models import AccountModel
from accounts.tests.utils import (  # user_admin_correct,; user_seller_correct,
    create_account_201_response_fields,
    email_conflict_detail,
    forbidden_details,
    get_admin_payload,
    get_seller_payload,
    unauthorized_details,
    username_conflict_detail,
)
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_409_CONFLICT,
)
from rest_framework.test import APITestCase


class TestAccountsPOST(APITestCase):
    PATH = "/accounts/"

    @classmethod
    def setUpTestData(cls) -> None:
        # Creating seller and seller token
        cls.seller_data = get_seller_payload()
        cls.seller: AccountModel = AccountModel.objects.create(**cls.seller_data)

        # Creating admin and admin token
        cls.admin_data = get_admin_payload()
        cls.admin: AccountModel = AccountModel.objects.create(**cls.admin_data)

    def test_if_creates_admin_without_store_id_201(self):

        # Authenticating with admin credentials
        self.client.force_authenticate(user=self.admin)

        data = get_admin_payload()

        response = self.client.post(self.PATH, data, format="json")
        output = response.json()

        self.assertEqual(response.headers["Content-Type"], "application/json")

        for field in create_account_201_response_fields:
            self.assertIn(field, output)

        self.assertNotIn("password", output)
        self.assertIsNone(output["store_id"])
        self.assertTrue(output["is_admin"])

    def test_if_creates_seller_without_store_id_201(self):

        # Authenticating with seller credentials
        self.client.force_authenticate(user=self.seller)

        data = get_seller_payload()

        response = self.client.post(self.PATH, data, format="json")
        output = response.json()

        self.assertEqual(response.headers["Content-Type"], "application/json")

        for field in create_account_201_response_fields:
            self.assertIn(field, output)

        self.assertNotIn("password", output)
        self.assertIsNone(output["store_id"])
        self.assertFalse(output["is_admin"])

    def test_if_evaluates_wrong_schema_400(self):

        # Authenticating with admin credentials
        self.client.force_authenticate(user=self.admin)

        data = get_seller_payload()

        # Popping one field and testing if returns correct message
        for field in data.keys():
            payload = {**data}
            payload.pop(field)

            response = self.client.post(self.PATH, data, format="json")
            output = response.json()

            self.assertEqual(response.headers["Content-Type"], "application/json")
            self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

            error_message = {field: ["This field is required."]}

            self.assertEqual(output, error_message)

    def test_if_evaluates_request_without_authorization_header_401(self):

        self.client.credentials(HTTP_AUTHORIZATION=None)

        data = get_seller_payload()

        response = self.client.post(self.PATH, data, format="json")
        output = response.json()

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(output, unauthorized_details)

    def test_if_seller_can_not_create_account_403(self):

        # Authenticating with seller credentials
        self.client.force_authenticate(user=self.seller)

        data = get_seller_payload()

        response = self.client.post(self.PATH, data, format="json")
        output = response.json()

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(output, forbidden_details)

    def test_if_evaluates_username_unicity_409(self):

        # Authenticating with admin credentials
        self.client.force_authenticate(user=self.admin)

        # Repeating just `username` to force unicity error
        data = {**get_admin_payload(), "username": self.admin.username}

        response = self.client.post(self.PATH, data, format="json")
        output = response.json()

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, HTTP_409_CONFLICT)
        self.assertEqual(output, username_conflict_detail)

    def test_if_evaluates_email_unicity_409(self):

        # Authenticating with admin credentials
        self.client.force_authenticate(user=self.admin)

        # Repeating just `email` to force unicity error
        data = {**get_admin_payload(), "email": self.admin.email}

        response = self.client.post(self.PATH, data, format="json")
        output = response.json()

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, HTTP_409_CONFLICT)
        self.assertEqual(output, email_conflict_detail)
