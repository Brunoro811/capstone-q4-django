from accounts.models import AccountModel
from accounts.tests.utils import user_admin_correct, user_seller_correct
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class TestAccounst(APITestCase):
    @classmethod
    def setUpTestData(cls):
        test_admin = AccountModel.objects.create_user(**user_admin_correct)
        test_seller = AccountModel.objects.create_user(**user_seller_correct)
        cls.admin_token = Token.objects.get_or_create(user=test_admin)[0].key
        cls.seller_token = Token.objects.get_or_create(user=test_seller)[0].key

    def test_if_cant_list_all_without_being_logged(self):
        response = self.client.get("/accounts/", format="json")

        self.assertEqual(response.status_code, 401)
        self.assertIn("detail", response.json())

    def test_if_can_list_all_users_as_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token)
        response = self.client.get("/accounts/", format="json")

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_if_cant_list_all_users_as_seller(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.seller_token)

        response = self.client.get("/accounts/", format="json")

        self.assertEqual(response.status_code, 403)
        self.assertIn("detail", response.json())
