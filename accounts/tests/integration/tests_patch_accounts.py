from accounts.models import AccountModel
from accounts.tests.utils import user_admin_correct, user_seller_correct
from rest_framework import status
from rest_framework.test import APITestCase


class AccountsUpdateTest(APITestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:
        
        # fields of user admin
        cls.user_admin_correct = user_admin_correct()

        cls.username_admin = cls.user_admin_correct['username']
        cls.password_admin = cls.user_admin_correct['password']
        cls.user_admin = AccountModel.objects.create_user(
            **cls.user_admin_correct
        )
        cls.user_login_admin = {
            "username":cls.username_admin,
            "password" : cls.password_admin
        }

        # fields of user seller
        cls.user_seller_correct = user_seller_correct()

        cls.username_seller = cls.user_seller_correct['username']
        cls.password_seller = cls.user_seller_correct['password']
        cls.user_seller = AccountModel.objects.create_user(
            **cls.user_seller_correct
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
            "last_name": "Alvaro",
            "is_seller": True,
        }
         
        self.client.credentials(HTTP_AUTHORIZATION="Token "+ token)
        response = self.client.patch("/accounts/", fields_to_update ,format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for key_field in fields_to_update:
            self.assertTrue( fields_to_update[key_field] ,response.json()[key_field])
        
        self.assertTrue( fields_to_update['first_name'] ,response.json()['first_name'])
        self.assertTrue( fields_to_update['last_name'] ,response.json()['last_name'])
        self.assertTrue( fields_to_update['is_seller'] ,response.json()['is_seller'])
        
        
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

    def test_seller_should_try_to_change_unauthorized_fields_and_returns_403 (self):

        token = self.client.post('/login/', self.user_login_seller , format='json').json()['token']

        fields_to_update = {
            "first_name": "João",
            "last_name": "Alvaro",
            "is_admin": True,
            "is_seller": False,
            "email": "joao@gmail.com",
            "username": "fulaninho",
        }
            
        expected_json = {
            "detail": "seller not authorized for this action.",
            "unauthorized_fields": set([
                "username",
                "email",
                "is_seller",
                "is_admin",
            ])
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token "+ token)
        response = self.client.patch("/accounts/", fields_to_update ,format='json')
        output = response.json()
        output['unauthorized_fields'] = set(output['unauthorized_fields'])
        self.assertEqual (response.status_code, status.HTTP_403_FORBIDDEN)
        
        self.assertEqual( expected_json , output)
        
    
    def test_admin_try_to_update_with_wrong_type_fields_return_code_400(self):
        
        token = self.client.post('/login/', self.user_login_admin , format='json').json()['token']

        fields_to_update = {
            "first_name": "first_name 2",
            "is_seller": 10
        }

        expected_json = {
            "is_seller": [
                "Must be a valid boolean."
            ]
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token "+ token)
        response = self.client.patch("/accounts/", fields_to_update ,format='json')

        self.assertEqual (response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual ( expected_json ,response.json())

