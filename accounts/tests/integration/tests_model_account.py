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

    def test_if_cant_get_one_user_without_being_logged(self):
        response = self.client.get("/api/accounts/", format="json")

        self.assertEqual(response.status_code, 401)
        self.assertIn("detail", response.json())

    def test_if_can_get_one_user_as_admin(self):
        user_id = Token.objects.get(key=self.seller_token).user.id
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token)
        response = self.client.get(f"/api/accounts/{user_id}", format="json")

        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.json())
        self.assertIn("username", response.json())
        self.assertIn("email", response.json())
        self.assertIn("is_admin", response.json())
        self.assertIn("is_seller", response.json())
        self.assertIn("first_name", response.json())
        self.assertIn("last_name", response.json())
        self.assertIn("created_at", response.json())

    def test_if_cant_get_one_user_as_seller(self):
        user_id = Token.objects.get(key=self.seller_token).user.id
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.seller_token)

        response = self.client.get(f"/api/accounts/{user_id}/", format="json")

        self.assertEqual(response.status_code, 403)
        self.assertIn("detail", response.json())

    def test_if_cant_get_one_user_if_user_dont_exists(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token)
        response = self.client.get(
            "/api/accounts/230d81bf-2092-420a-a310-505ed9a1c243/", format="json"
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("detail", response.json())
