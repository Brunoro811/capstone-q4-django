from uuid import UUID

from categorys.models import CategoryModel
from django.test import TestCase
from products.models import ProductModel
from products.tests.utils import product_shirt
from stores.models import StoreModel
from stores.tests.utils import store_correct
from variations.models import VariationModel
from variations.tests.utils import generate_variation_for_size


class VariationsModelTest(TestCase):
    
    @classmethod 
    def setUpTestData(cls) -> None:
        
        cls.category = CategoryModel.objects.create(**{'name': 'Camiseta'})

        cls.store = StoreModel.objects.create(**store_correct)
        
        cls.product_shirt = ProductModel.objects.create(
            **product_shirt(),
            category_id = cls.category,
            store_id=cls.store   
        )
        cls.variation = generate_variation_for_size()
        cls.variation_obj = VariationModel.objects.create(
            **cls.variation,
            product_id=cls.product_shirt
        )
        
        
        return super().setUpTestData()

    def test_model_variation_fields(self):
        
        self.assertIsInstance( self.variation_obj.id , UUID )

        self.assertIsInstance( self.variation_obj.size , str )
        self.assertEqual( self.variation_obj.size, self.variation['size'] )

        self.assertIsInstance( self.variation_obj.quantity , int )
        self.assertEqual( self.variation_obj.quantity, self.variation['quantity'] )
        
        self.assertIsInstance( self.variation_obj.color , str )
        self.assertEqual( self.variation_obj.color, self.variation['color'] )

    def test_model_variation_foregnkey_product(self):
        
        self.assertIsInstance(self.variation_obj.product_id, ProductModel)
