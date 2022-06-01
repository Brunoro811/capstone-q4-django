from datetime import datetime
from uuid import UUID

from accounts.models import AccountModel
from accounts.tests.utils import user_seller_correct
from categories.models import CategoryModel
from django.test import TestCase
from orders.models import OrdersModel, OrderVariationsModel
from orders.tests.utils import generate_order
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

        cls.seller = AccountModel.objects.create(
            **user_seller_correct(),
            store_id=cls.store
            )

        cls.orders =  {
            **generate_order(),
            'seller_id': cls.seller ,
            'store_id': cls.store ,
            'total_value': 200.1
        }
        cls.orders_obj = OrdersModel.objects.create(**cls.orders)

        cls.orders_products = {}
        
        return super().setUpTestData()  
    
    def test_model_orders_fields(self):
        
        self.assertIsInstance( self.orders_obj, OrdersModel )
        
        self.assertIsInstance( self.orders_obj.id, UUID )
        
        self.assertIsInstance( self.orders_obj.total_value, float )
        self.assertEqual( self.orders_obj.total_value, self.orders['total_value'] )

        self.assertIsInstance( self.orders_obj.created_at, datetime )
        
        self.assertIsInstance( self.orders_obj.seller_id.id, UUID )
        self.assertIsInstance( self.orders_obj.seller_id, AccountModel )

        self.assertIsInstance( self.orders_obj.store_id.id, UUID )
        self.assertIsInstance( self.orders_obj.store_id, StoreModel )



class OrdersVariationsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.category = CategoryModel.objects.create(**{'name': 'Camiseta'})

        cls.store = StoreModel.objects.create(**store_correct)

        cls.seller = AccountModel.objects.create(
            **user_seller_correct(),
            store_id=cls.store
            )
        
        cls.product_shirt_obj = ProductModel.objects.create(
            **product_shirt(),
            category_id = cls.category,
            store_id=cls.store   
        )

        
        cls.variation = {
            **generate_variation_for_size(),
            'product_id': cls.product_shirt_obj
        }
        
        cls.variation_obj = VariationModel.objects.create(
            **cls.variation
        )

        cls.orders =  {
            **generate_order(),
            'seller_id': cls.seller ,
            'store_id': cls.store ,
            'total_value': 200.1
        }
        cls.orders_obj = OrdersModel.objects.create(**cls.orders)
        
        cls.orders_variations ={
                'sale_value': cls.product_shirt_obj.sale_value_retail ,
                'quantity':3,
                'order_id': cls.orders_obj,
                'variation_id': cls.variation_obj
            }

        cls.orders_variations_obj = OrderVariationsModel.objects.create(**cls.orders_variations)
        
        return super().setUpTestData()  
    
    def test_model_orders_variations_fields(self):

        self.assertIsInstance(self.orders_variations_obj.id , UUID)
        
        self.assertIsInstance(self.orders_variations_obj.sale_value, float)
        self.assertEqual(self.orders_variations_obj.sale_value, self.orders_variations['sale_value'])

        self.assertIsInstance(self.orders_variations_obj.quantity, int)
        self.assertEqual(self.orders_variations_obj.quantity, self.orders_variations['quantity'])

        self.assertIsInstance(self.orders_variations_obj.order_id, OrdersModel)

        self.assertIsInstance(self.orders_variations_obj.variation_id, VariationModel)
        
        