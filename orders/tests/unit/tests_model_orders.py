from categories.models import CategoryModel
from django.test import TestCase
from products.models import ProductModel
from products.tests.utils import product_shirt
from stores.models import StoreModel
from stores.tests.utils import store_correct
from variations.models import VariationModel
from variations.tests.utils import generate_variation_for_size


class OrdersModelTest(TestCase):

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
    
    def test_model_fields(self):
        ...
