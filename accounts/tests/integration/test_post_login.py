from accounts.models import AccountModel
from accounts.tests.utils import fields_get_one_user
from accounts.tests.utils import \
    user_admin_correct as function_user_admin_correct
from accounts.tests.utils import \
    user_seller_correct as function_user_seller_correct
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class TestAccounst(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user_admin_correct = function_user_admin_correct()
        user_seller_correct = function_user_seller_correct()

        cls.login_seller = {
            "username": user_seller_correct["username"],
            "password": user_seller_correct["password"],
        }
        cls.login_admin = {
            "username": user_admin_correct["username"],
            "password": user_admin_correct["password"],
        }
        cls.test_admin = AccountModel.objects.create_user(**user_admin_correct)
        cls.test_seller = AccountModel.objects.create_user(**user_seller_correct)

    def test_if_user_can_login_with_correct_admin_username_and_password(self):
        response = self.client.post("/login/", self.login_admin, format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.json())
        self.assertIsInstance(response.json()["token"], str)

    def test_if_user_can_login_with_correct_seller_username_and_password(self):
        response = self.client.post("/login/", self.login_seller, format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.json())
        self.assertIsInstance(response.json()["token"], str)

    def test_if_user_cant_login_missing_password_field(self):
        response = self.client.post(
            "/login/",
            {
                "username": self.login_admin["username"],
            },
            format="json",
        )

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.json())
        self.assertEqual(["This field is required."], response.json()["password"])

    def test_if_user_cant_login_missing_username_field(self):
        response = self.client.post(
            "/login/",
            {
                "password": self.login_admin["password"],
            },
            format="json",
        )
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.json())
        self.assertEqual(response.json()["username"], ["This field is required."])

    def test_if_user_cant_login_with_wrong_password(self):
        response = self.client.post(
            "/login/",
            {
                "username": self.login_admin["username"],
                "password": self.login_admin["password"] + "a",
            },
            format="json",
        )
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.json())
        self.assertEqual(response.json()["detail"], "Invalid credentials.")

    def test_if_user_cant_login_with_wrong_username(self):
        response = self.client.post(
            "/login/",
            {
                "username": self.login_admin["username"] + "a",
                "password": self.login_admin["password"],
            },
            format="json",
        )
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.json())
        self.assertEqual(response.json()["detail"], "Invalid credentials.")
