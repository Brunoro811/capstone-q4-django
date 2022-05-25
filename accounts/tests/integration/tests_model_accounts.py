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

    def test_if_user_can_login_with_correct_email_and_password(self):
        response = self.client.post(
            "/login/",
            {
                "username": user_admin_correct["username"],
                "password": user_admin_correct["password"],
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

    def test_if_user_cant_login_missing_password(self):
        response = self.client.post(
            "/login/",
            {"username": user_admin_correct["username"]},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("password", response.json())

    def test_if_user_cant_login_missing_username(self):
        response = self.client.post(
            "/login/",
            {"password": user_admin_correct["password"]},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("username", response.json())

    def test_if_user_cant_login_with_wrong_password(self):
        response = self.client.post(
            "/login/",
            {
                "username": user_admin_correct["username"],
                "password": "wordGeneratorSevenPointO",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn("detail", response.json())

    def test_if_user_cant_login_with_wrong_email(self):
        response = self.client.post(
            "/login/",
            {
                "username": "highestInTheRoom",
                "password": user_admin_correct["password"],
            },
            format="json",
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn("detail", response.json())
