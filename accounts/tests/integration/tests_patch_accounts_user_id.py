from accounts.models import AccountModel
from accounts.tests.utils import user_admin_correct, user_seller_correct
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class TestAccounts(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.seller_data = user_seller_correct
        cls.seller: AccountModel = AccountModel.objects.create(**cls.seller_data)

        cls.admin_data = user_admin_correct
        cls.admin: AccountModel = AccountModel.objects.create(**cls.admin_data)

    def test_if_can_update_user_by_id_as_admin(self):   

        self.client.force_authenticate(user=self.admin)

        response = self.client.patch(f"/accounts/{self.seller.id}", self.seller_data,format="json")
        
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.json())
        self.assertIn("username", response.json())
        self.assertIn("email", response.json())
        self.assertIn("is_admin", response.json())
        self.assertIn("is_seller", response.json())
        self.assertIn("first_name", response.json())
        self.assertIn("last_name", response.json())
        self.assertIn("created_at", response.json())
        
    def test_if_cant_update_user_by_id_without_being_logged(self):
        response = self.client.patch(f"/accounts/{self.seller.id}", self.seller_data,format="json")
        

        self.assertEqual(response.status_code, 401)
        self.assertIn("detail", response.json())

    def test_if_cant_update_user_by_id_as_seller(self):
        self.client.force_authenticate(user=self.seller)

        response = self.client.patch(f"/accounts/{self.seller.id}", self.seller_data,format="json")
        
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, 403)
        self.assertIn("detail", response.json())

    def test_if_cant_update_user_by_id_if_user_dont_exists(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.patch(f"/accounts/230d81bf-2092-420a-a310-505ed9a1c243", self.seller_data, format="json")
        
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, 404)
        self.assertIn("detail", response.json())

    def test_cant_update_user_by_id_if_user_already_exists(self):
        self.client.force_authenticate(user=self.admin)

        data = {**user_admin_correct, "username": self.admin.username}

        response = self.client.patch(f"/accounts/{self.seller.id}", data, format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, 409)
        self.assertIn("detail", response.json())

    def test_cant_update_user_by_id_if_email_already_exists(self):
        self.client.force_authenticate(user=self.admin)

        data = {**user_admin_correct, "email": self.admin.email}

        response = self.client.patch(f"/accounts/{self.seller.id}", data, format="json")

        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, 409)
        self.assertIn("detail", response.json())


