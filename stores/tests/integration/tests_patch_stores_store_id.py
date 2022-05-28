from uuid import uuid4

from accounts.models import AccountModel
from accounts.tests.utils import get_admin_payload, get_seller_payload
from rest_framework.status import (HTTP_200_OK, HTTP_401_UNAUTHORIZED,
                                   HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND,
                                   HTTP_409_CONFLICT)
from rest_framework.test import APITestCase
from stores.models import StoreModel
from stores.tests.utils import (forbidden_details, get_store_payload,
                                not_found_details, store_name_conflict_detais,
                                unauthorized_details,
                                update_store_200_response_fields)


class TestStorePATCH(APITestCase):
    PATH = "/stores"

    @classmethod
    def setUpTestData(cls) -> None:
        # Creating seller
        cls.seller_data = get_seller_payload()
        cls.seller: AccountModel = AccountModel.objects.create(**cls.seller_data)

        # Creating admin
        cls.admin_data = get_admin_payload()
        cls.admin: AccountModel = AccountModel.objects.create(**cls.admin_data)

        # Creating store
        cls.store_data = get_store_payload()
        cls.store: StoreModel = StoreModel.objects.create(**cls.store_data)
    def test_if_updates_correctly_200(self):
        # Authenticating with admin credentials
        self.client.force_authenticate(user=self.admin)

        data = get_store_payload()

        # Checking individualy if the updatable fields may be updated
        for field, value in data.items():
            payload = {field: value}
            
            response = self.client.patch(
                f"{self.PATH}/{self.store.id}/", payload, format="json"
            )
            
            output = response.json()

            self.assertEqual(response.headers["Content-Type"], "application/json")
            self.assertEqual(response.status_code, HTTP_200_OK)

            # Testing if updated field is returned
            self.assertEqual(output[field], value)

            # Testing if response payload has only correct fields
            self.assertEqual(set(output), set(update_store_200_response_fields))

    def test_if_patch_store_evaluates_request_without_authorization_header_401(self):

        self.client.credentials(HTTP_AUTHORIZATION="")

        data = get_store_payload()

        response = self.client.patch(
            f"{self.PATH}/{self.store.id}/", data, format="json"
        )
        output = response.json()
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(output, unauthorized_details)

    def test_if_seller_can_not_create_store_403(self):

        # Authenticating with seller credentials
        self.client.force_authenticate(user=self.seller)

        data = get_store_payload()

        response = self.client.patch(
            f"{self.PATH}/{self.store.id}/", data, format="json"
        )
        output = response.json()

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(output, forbidden_details)

    def test_not_found_store_response_store_404(self):

        # Authenticating with seller credentials
        self.client.force_authenticate(user=self.admin)

        data = get_store_payload()

        response = self.client.patch(
            f"{self.PATH}/{uuid4()}/", data, format="json"
        )
        output = response.json()

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
        self.assertEqual(output, not_found_details)

    def test_if_evaluates_store_name_unicity_409(self):

        # Authenticating with admin credentials
        self.client.force_authenticate(user=self.admin)

        # Creating new store
        new_store: StoreModel = StoreModel.objects.create(**get_store_payload())

        # Repeating `name` to force unicity error
        data = {"name": new_store.name}

        response = self.client.patch(
            f"{self.PATH}/{self.store.id}/", data, format="json"
        )
        output = response.json()

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, HTTP_409_CONFLICT)
        self.assertEqual(output, store_name_conflict_detais)
