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
            'seller': cls.seller ,
            'store': cls.store ,
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
        
        self.assertIsInstance( self.orders_obj.seller.id, UUID )
        self.assertIsInstance( self.orders_obj.seller, AccountModel )

        self.assertIsInstance( self.orders_obj.store.id, UUID )
        self.assertIsInstance( self.orders_obj.store, StoreModel )



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

        
        cls.variation_P = {
            **generate_variation_for_size(),
            'product_id': cls.product_shirt_obj
        }
        
        
        cls.variation_obj_P = VariationModel.objects.create(
            **cls.variation_P
        )

        cls.orders =  {
            'seller': cls.seller ,
            'store': cls.store ,
            'total_value': 200.1
        }
        cls.orders_obj = OrdersModel.objects.create(**cls.orders)
        
        cls.orders_variations = {
                'sale_value': cls.product_shirt_obj.sale_value_retail ,
                'quantity':3,
                'order': cls.orders_obj,
                'variation': cls.variation_obj_P
            }

        cls.orders_variations_obj = OrderVariationsModel.objects.create(**cls.orders_variations)
        cls.list_orders_variation_created = [cls.orders_variations_obj]

        
        return super().setUpTestData()  
    
    def test_model_orders_variations_fields(self):

        self.assertIsInstance(self.orders_variations_obj.id , UUID)
        
        self.assertIsInstance(self.orders_variations_obj.sale_value, float)
        self.assertEqual(self.orders_variations_obj.sale_value, self.orders_variations['sale_value'])

        self.assertIsInstance(self.orders_variations_obj.quantity, int)
        self.assertEqual(self.orders_variations_obj.quantity, self.orders_variations['quantity'])

        self.assertIsInstance(self.orders_variations_obj.order, OrdersModel)

        self.assertIsInstance(self.orders_variations_obj.variation, VariationModel)
        
    def test_model_orders_variations_relationship_many_to_many(self):

        self.orders =  {
            'seller': self.seller ,
            'store': self.store ,
            'total_value': 159.99
        }
        self.orders_obj = OrdersModel.objects.create(**self.orders)

        self.variation_M = {
            **generate_variation_for_size('M'),
            'product_id': self.product_shirt_obj
        }

        self.variation_obj_M = VariationModel.objects.create(
            **self.variation_M
        )
        
        self.orders_variations_list = [
            OrderVariationsModel(**{
                'sale_value': self.product_shirt_obj.sale_value_retail ,
                'quantity':3,
                'order': self.orders_obj,
                'variation': self.variation_obj_M
            }),
            OrderVariationsModel(**{
                'sale_value': self.product_shirt_obj.sale_value_retail ,
                'quantity':2,
                'order': self.orders_obj,
                'variation': self.variation_obj_P
            })
        ]
        
        self.order_list_variation = OrderVariationsModel.objects.bulk_create(self.orders_variations_list)
            
        list_id_variation_order = [ variation.id for variation in self.orders_obj.variations.all() ]
        list_id_variation = [ variation.variation.id for variation in self.order_list_variation ]
        
        for variation in list_id_variation_order:
            print(f"\n List: { variation in list_id_variation } \n")

    