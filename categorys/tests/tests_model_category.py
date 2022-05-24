from categorys.models import CategoryModel
from django.db.models import Model
from django.test import TestCase


class CategoryModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:
        cls.name = 'Vestidos'
        cls.category_object = CategoryModel.objects.create(name=cls.name)
        return super().setUpTestData()

    def test_model_category_fields(self):
        
        self.assertIsInstance(self.name, str)
        self.assertEqual(self.name,self.category_object.name)

        self.assertIsInstance(self.category_object, Model)
