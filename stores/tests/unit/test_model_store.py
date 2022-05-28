import uuid
from datetime import datetime

from accounts.models import AccountModel
from accounts.tests.utils import user_admin_correct
from django.db.models import Model
from django.test import TestCase
from stores.models import StoreModel
from stores.tests.utils import store_correct


class StoreModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:
        
        cls.name = store_correct['name']
        cls.street = store_correct['street']    
        cls.number = store_correct['number']
        cls.zip_code = store_correct['zip_code']
        cls.state = store_correct['state']
        cls.other_information = store_correct['other_information']
        
        cls.store_object = StoreModel.objects.create(**store_correct)
        cls.user_admin = AccountModel.objects.create_user(**user_admin_correct(), store_id=cls.store_object)
        
        return super().setUpTestData()

    def test_model_store_fields(self):
        
        self.assertIsInstance(self.store_object.id, uuid.UUID)

        self.assertIsInstance(self.name, str)
        self.assertEqual(self.name, self.store_object.name)

        self.assertIsInstance(self.street, str)
        self.assertEqual(self.street, self.store_object.street)

        self.assertIsInstance(int(self.number), int)
        self.assertEqual(self.number, self.store_object.number)

        self.assertIsInstance(self.zip_code, str)
        self.assertEqual(self.zip_code, self.store_object.zip_code)

        self.assertIsInstance(self.state, str)
        self.assertEqual(self.state, self.store_object.state)

        self.assertIsInstance(self.other_information, str)
        self.assertEqual(self.other_information, self.store_object.other_information)

        self.assertIsInstance(self.store_object, Model)
