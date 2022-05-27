import uuid

from accounts.models import AccountModel
from accounts.tests.utils import user_admin_correct
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractUser
from django.test import TestCase
from stores.models import StoreModel
from stores.tests.utils import store_correct


class AccountsModelTest(TestCase):
    

    @classmethod
    def setUpTestData(cls) -> None:
        
        cls.user_admin_correct = user_admin_correct()

        cls.username = cls.user_admin_correct['username']
        cls.email = cls.user_admin_correct['email']
        cls.password = cls.user_admin_correct['password']
        cls.is_admin = cls.user_admin_correct['is_admin']
        cls.is_seller = cls.user_admin_correct['is_seller']
        cls.first_name = cls.user_admin_correct['first_name']
        cls.last_name = cls.user_admin_correct['last_name']

        cls.store_object = StoreModel.objects.create(**store_correct)
        
        cls.user_admin_correct_object = AccountModel.objects.create_user(**cls.user_admin_correct, store=cls.store_object)
        
        return super().setUpTestData()
    
    def test_model_accounts_fields(self):
        
        self.assertIsInstance(self.user_admin_correct_object.id, uuid.UUID)
        
        self.assertIsInstance(self.user_admin_correct_object.username, str)
        self.assertEqual(self.user_admin_correct_object.username, self.username)

        self.assertIsInstance(self.user_admin_correct_object.email, str)
        self.assertEqual(self.user_admin_correct_object.email, self.email)

        self.assertIsInstance(self.user_admin_correct_object.password, str)
        self.assertTrue(check_password(self.password,self.user_admin_correct_object.password))

        self.assertIsInstance(self.is_admin, bool)
        self.assertEqual(self.is_admin,self.user_admin_correct_object.is_admin)

        self.assertIsInstance(self.is_seller, bool)
        self.assertEqual(self.is_seller,self.user_admin_correct_object.is_seller)

        self.assertIsInstance(self.first_name, str)
        self.assertEqual(self.first_name, self.user_admin_correct_object.first_name)

        self.assertIsInstance(self.last_name, str)
        self.assertEqual(self.last_name, self.user_admin_correct_object.last_name)
        
        self.assertIsInstance(self.user_admin_correct_object, AbstractUser)

    def test_model_accounts_foreignkey_store_id_field(self):
        
        self.assertIsInstance(self.user_admin_correct_object.store , StoreModel)
