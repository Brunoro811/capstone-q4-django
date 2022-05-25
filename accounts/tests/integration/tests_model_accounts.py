from accounts.models import AccountModel
from accounts.tests.utils import (
    fields_get_one_user,
    user_admin_correct,
    user_seller_correct,
)
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class TestAccounst(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.login_seller = {
            "email": user_seller_correct["email"],
            "password": user_seller_correct["password"],
        }
        cls.login_admin = {
            "email": user_admin_correct["email"],
            "password": user_admin_correct["password"],
        }
        cls.test_admin = AccountModel.objects.create_user(**user_admin_correct)
        cls.test_seller = AccountModel.objects.create_user(**user_seller_correct)

    def test_if_user_can_login_with_correct_admin_email_and_password(self):
        response = self.client.post(
            "/login/",
            {
                "username": user_admin_correct["username"],
                "password": user_admin_correct["password"],
            },
            format="json",
        )
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.json())
        self.assertIsInstance(response.json()["token"], str)

    def test_if_user_can_login_with_correct_seller_email_and_password(self):
        response = self.client.post(
            "/login/",
            {
                "username": user_seller_correct["username"],
                "password": user_seller_correct["password"],
            },
            format="json",
        )
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.json())
        self.assertIsInstance(response.json()["token"], str)

    def test_if_user_cant_login_missing_password(self):
        response = self.client.post(
            "/login/",
            {
                "username": user_admin_correct["username"],
            },
            format="json",
        )
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.json())
        self.assertIn(["This field is required."], response.json()["password"])

    def test_if_user_cant_login_missing_username(self):
        response = self.client.post(
            "/login/",
            {
                "password": user_admin_correct["password"],
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
                "username": user_admin_correct["username"],
                "password": user_admin_correct["password"] + "a",
            },
            format="json",
        )
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.json())
        self.assertEqual(response.json()["details"], "Invalid credentials.")

    def test_if_user_cant_login_with_wrong_username(self):
        response = self.client.post(
            "/login/",
            {
                "username": user_admin_correct["username"] + "a",
                "password": user_admin_correct["password"],
            },
            format="json",
        )
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.json())
        self.assertEqual(response.json()["detail"], "Invalid credentials.")

    def test_if_cant_list_all_without_authorization_header(self):
        response = self.client.get("/accounts/", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.json())
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )

    def test_if_can_list_all_users_with_admin_account(self):
        self.client.force_authenticate(user=self.test_admin)
        response = self.client.get("/accounts/", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), list)

    def test_if_cant_list_all_users_as_seller(self):
        self.client.force_authenticate(user=self.test_seller)
        response = self.client.get("/accounts/", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.json())
        self.assertEqual(
            response.json()["detail"],
            "You do not have permission to perform this action.",
        )

    def test_if_cant_get_one_user_without_authorization_header(self):
        response = self.client.get("/accounts/", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.json())
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )

    def test_if_can_get_one_user_as_admin(self):
        user_id = str(self.test_admin.id)
        self.client.force_authenticate(user=self.test_admin)
        response = self.client.get(f"/accounts/{user_id}/", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field in fields_get_one_user:
            self.assertIn(field, response.json())

    def test_if_cant_get_one_user_as_seller(self):
        user_id = Token.objects.get(key=self.seller_token).user.id
        self.client.force_authenticate(user=self.test_seller)
        response = self.client.get(f"/accounts/{user_id}/", format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.json())
        self.assertEqual(
            response.json()["detail"],
            "You do not have permission to perform this action.",
        )

    def test_if_cant_get_one_user_if_user_dont_exists(self):
        self.client.force_authenticate(user=self.test_admin)
        response = self.client.get(
            "/accounts/230d81bf-2092-420a-a310-505ed9a1c243/", format="json"
        )
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.json())
        self.assertEqual(response.json()["detail"], "Not found.")
