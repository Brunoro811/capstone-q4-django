from accounts.tests.utils import user_admin_correct, user_seller_correct
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from stores.models import StoreModel
from stores.tests.utils import store_correct


class TestAccounst(APITestCase):
    @classmethod
    def setUpTestData(cls):
        test_admin = StoreModel.objects.create(**user_admin_correct)
        test_seller = StoreModel.objects.create(**user_seller_correct)
        cls.admin_token = Token.objects.get_or_create(user=test_admin)[0].key
        cls.seller_token = Token.objects.get_or_create(user=test_seller)[0].key

    def test_if_store_can_be_created_with_missing_fields(self):
        del store_correct["name"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token)
        response = self.client.post(
            "/stores/",
            {**store_correct},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.json())

    def test_if_store_cant_be_created_without_being_logged(self):
        response = self.client.post("/stores/", {**store_correct}, format="json")

        self.assertEqual(response.status_code, 401)
        self.assertIn("detail", response.json())

    def test_if_store_cant_be_created_logged_as_seller(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.seller_token)
        response = self.client.post("/stores/", {**store_correct}, format="json")

        self.assertEqual(response.status_code, 403)
        self.assertIn("detail", response.json())

    def test_is_store_can_be_created_with_correct_fields_and_admin_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token)
        response = self.client.post(
            "/stores/",
            {**store_correct},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())
        self.assertIn("name", response.json())
        self.assertIn("state", response.json())
        self.assertIn("street", response.json())
        self.assertIn("number", response.json())
        self.assertIn("zip_code", response.json())
        self.assertIn("is_active", response.json())
        self.assertIn("other_information", response.json())
        self.assertIn("created_at", response.json())
        self.assertIn("updated_at", response.json())

    def test_if_new_store_cant_be_created_with_existing_name(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token)
        self.client.post("/stores/", {**store_correct}, format="json")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token)
        response = self.client.post("/stores/", {**store_correct}, format="json")

        self.assertEqual(response.status_code, 409)
        self.assertIn("detail", response.json())
