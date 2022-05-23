import uuid

from accounts.models import AccountsModel
from accounts.tests.utils import user_admin_correct
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractUser
from django.test import TestCase


class AccountsModelTest(TestCase):
    

    @classmethod
    def setUpTestData(cls) -> None:
        
        cls.email = user_admin_correct['email']
        cls.password = user_admin_correct['password']
        cls.user_admin_correct_object = AccountsModel.objects.create(**user_admin_correct)
        
        return super().setUpTestData()
    
    def test_model_accounts_fields(self):
        
        self.assertIsInstance(self.user_admin_correct_object.email, str)
        self.assertEqual(self.user_admin_correct_object.email, self.email)
        
        self.assertIsInstance(self.user_admin_correct_object.password, str)
        self.assertTrue(check_password(self.user_admin_correct_object.password,self.password))

        self.assertIsInstance(self.user_admin_correct_object.id, uuid.UUID)
        self.assertIsInstance(self.user_admin_correct_object, AbstractUser)
