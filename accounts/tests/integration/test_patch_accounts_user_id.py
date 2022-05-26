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
        ...


    def test_if_cant_update_user_by_id_without_being_logged(self):
        ...

    def test_if_cant_update_user_by_id_as_seller(self):
        ...

    def test_if_cant_update_user_by_id_if_user_dont_exists(self):
        ...

    def test_cant_update_user_by_id_if_user_already_exists(self):
        ...
    def test_cant_update_user_by_id_if_email_already_exists(self):
        ...



