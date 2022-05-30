from uuid import UUID

from django.test import TestCase
from products.models import ProductsModel
from products.tests.utils import value_product


class ProductModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:

        cls.product_shirt = value_product()
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

        self.assertIsInstance(self.product_shirt, ProductsModel )
        
        self.assertIsInstance(self.product_shirt.name, str )
        self.assertEqual(self.product_shirt.name, self.name)

        self.assertIsInstance(self.product_shirt.cost_value, float )
        self.assertEqual(self.product_shirt.cost_value, self.cost_value)

        self.assertIsInstance(self.product_shirt.sale_value_retail, float )
        self.assertEqual(self.product_shirt.cost_vasale_value_retaillue, self.sale_value_retail)

        self.assertIsInstance(self.product_shirt.sale_value_wholesale, float )
        self.assertEqual(self.product_shirt.sale_value_wholesale, self.sale_value_wholesale)

        self.assertIsInstance(self.product_shirt.store_id, UUID )
        self.assertEqual(self.product_shirt.store_id, self.store_id)

        self.assertIsInstance(self.product_shirt.category_id, UUID )
        self.assertEqual(self.product_shirt.category_id, self.category_id)

        self.assertIsInstance(self.product_shirt.quantity_wholesale, int )
        self.assertEqual(self.product_shirt.quantity_wholesale, self.quantity_wholesale)
