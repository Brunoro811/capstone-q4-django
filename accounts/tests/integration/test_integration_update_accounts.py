from accounts.models import AccountModel
from accounts.tests.utils import user_admin_correct, user_seller_correct
from rest_framework import status
from rest_framework.test import APITestCase


class AccountsUpdateTest(APITestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:


        cls.username_admin = user_admin_correct['username']
        cls.password_admin = user_admin_correct['password']
        cls.user_admin = AccountModel.objects.create_user(
            **user_admin_correct
        )
        cls.user_login_admin = {
            "username":cls.username_admin,
            "password" : cls.password_admin
        }

        cls.username_seller = user_seller_correct['username']
        cls.password_seller = user_seller_correct['password']
        cls.user_seller = AccountModel.objects.create_user(
            **user_seller_correct
        )
        cls.user_login_seller = {
            'username': cls.username_seller,
            'password': cls.password_seller,
        }
        

        return super().setUpTestData()

    def test_try_to_update_user_without_passing_the_token_returns_401(self):
        
        fields_to_update = {
            "first_name": "João",
            "last_name": "Alvaro"
        }

        response = self.client.patch("/accounts/", fields_to_update ,format='json')

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
        response = self.client.patch("/accounts/", fields_to_update ,format='json')

        expected_json = {
            "detail": "Invalid token header. No credentials provided."
        }

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(expected_json,response.json())

    
    def test_should_to_user_by_passing_the_admin_token_and_returning_code_200 (self):
        
        token = self.client.post('/login/', self.user_login_admin, format='json').json()['token']
        fields_to_update = {
            "first_name": "João",
            "last_name": "Alvaro"
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token "+ token)
        response = self.client.patch("/accounts/", fields_to_update ,format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for key_field in fields_to_update:
            self.assertTrue( fields_to_update[key_field] ,response.json()[key_field])
        
        self.assertTrue( fields_to_update['first_name'] ,response.json()['first_name'])
        self.assertTrue( fields_to_update['last_name'] ,response.json()['last_name'])
        
    def test_should_to_user_by_passing_the_seller_token_and_returning_code_200 (self):

        token = self.client.post('/login/', self.user_login_seller , format='json').json()['token']

        fields_to_update = {
            "first_name": "João2",
            "last_name": "Alvaro2"
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token "+ token)
        response = self.client.patch("/accounts/", fields_to_update ,format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for key_field in fields_to_update:
            self.assertTrue( fields_to_update[key_field] ,response.json()[key_field])
    
        self.assertTrue( fields_to_update['first_name'] ,response.json()['first_name'])
        self.assertTrue( fields_to_update['last_name'] ,response.json()['last_name'])
