from uuid import UUID

from categories.models import CategoryModel
from django.test import TestCase
from products.models import ProductModel
from products.tests.utils import product_shirt
from stores.models import StoreModel
from stores.tests.utils import store_correct


class ProductModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:
        
        # create store and category
        cls.store_created = StoreModel.objects.create(**store_correct)
        cls.category_created = CategoryModel.objects.create(**{'name': "Vestidos"})
        
        cls.product_shirt = ProductModel.objects.create(
            **product_shirt(), 
            store_id= cls.store_created,
            category_id= cls.category_created,
        )

        cls.name = cls.product_shirt.name
        cls.cost_value = cls.product_shirt.cost_value
        cls.sale_value_retail = cls.product_shirt.sale_value_retail
        cls.sale_value_wholesale = cls.product_shirt.sale_value_wholesale
        cls.store_id = cls.product_shirt.store_id
        cls.category_id = cls.product_shirt.category_id
        cls.quantity_wholesale = cls.product_shirt.quantity_wholesale
        
        return super().setUpTestData()  
    
    def test_model_products_fields(self):
        
        self.assertIsInstance(self.product_shirt.id, UUID)

        self.assertIsInstance(self.product_shirt, ProductModel )
        
        self.assertIsInstance(self.product_shirt.name, str )
        self.assertEqual(self.product_shirt.name, self.name)

        self.assertIsInstance(self.product_shirt.cost_value, float )
        self.assertEqual(self.product_shirt.cost_value, self.cost_value)

        self.assertIsInstance(self.product_shirt.sale_value_retail, float )
        self.assertEqual(self.product_shirt.sale_value_retail, self.sale_value_retail)

        self.assertIsInstance(self.product_shirt.sale_value_wholesale, float )
        self.assertEqual(self.product_shirt.sale_value_wholesale, self.sale_value_wholesale)

        self.assertIsInstance(self.product_shirt.quantity_wholesale, int )
        self.assertEqual(self.product_shirt.quantity_wholesale, self.quantity_wholesale)

        self.assertIsInstance(self.product_shirt.store_id.id, UUID )
        self.assertEqual(self.product_shirt.store_id, self.store_id)

        self.assertIsInstance(self.product_shirt.category_id.id, UUID )
        self.assertEqual(self.product_shirt.category_id, self.category_id)
