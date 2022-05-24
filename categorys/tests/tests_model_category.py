from categorys.models import CategoryModel
from django.test import TestCase


class CategoryModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:
        cls.name = 'Vestidos'
        cls.category_object = CategoryModel.objects.create(name=cls.category)
        return super().setUpTestData()

    def test_model_category_fields(self):
        
        self.assertIsInstance(self.category, str)
        self.assertEqual(self.category,self.category_object.name)
        