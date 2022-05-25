from accounts.models import AccountModel
from accounts.tests.utils import user_admin_correct
from rest_framework import status
from rest_framework.test import APITestCase


class AccountsUpdateTest(APITestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:

        cls.username = user_admin_correct['username']
        cls.password = user_admin_correct['password']

        cls.super_user_admin = AccountModel.objects.create_superuser(
            username=cls.username,
            password=cls.password
        )

        cls.user_login = {
            'username': cls.username,
            'password': cls.password,
        }
        return super().setUpTestData()

    def test_try_to_update_user_without_passing_the_token_returns_401(self):
        
        fields_to_update = {
            "first_name": "João",
            "last_name": "Alvaro"
        }

        response = self.client.patch("/api/accounts/", fields_to_update ,format='json')

        expected_json = {
            "detail": "Authentication credentials were not provided."
        }

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(expected_json,response.json())
    
    def test_try_to_update_user_passing_the_empty_token_returns_401(self):
        
        fields_to_update = {
            "first_name": "João",
            "last_name": "Alvaro"
        }
        
        token = ""
        self.client.credentials(HTTP_AUTHORIZATION="Token "+ token)
        response = self.client.patch("/api/accounts/", fields_to_update ,format='json')

        expected_json = {
            "detail": "Invalid token header. No credentials provided."
        }

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(expected_json,response.json())

    
    def test_should_to_user_by_passing_the_admin_token_and_returning_code_200 (self):
        
        token = self.client.post('/api/login/', self.user_login, format='json').json()['token']

        fields_to_update = {
            "first_name": "João",
            "last_name": "Alvaro"
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token "+ token)
        response = self.client.patch("/api/accounts/", fields_to_update ,format='json')

        print(f"\n Saida: {response.status_code}")
        print(f"\n Saida: {response.json()}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(fields_to_update,response.json())
