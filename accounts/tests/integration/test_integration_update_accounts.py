from accounts.models import AccountModel
from accounts.tests.utils import user_admin_correct
from rest_framework.test import APITestCase


class AccountsUpdateTest(APITestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:
        
        cls.super_user_admin = AccountModel.objects.create_superuser(
            username=user_admin_correct['username'],
            password=user_admin_correct['password']
        )
        return super().setUpTestData()
