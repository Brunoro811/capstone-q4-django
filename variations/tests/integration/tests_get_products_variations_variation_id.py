# [] 200 OK
# [] 401 UNAUTHORIZED
# [] 404 Not Found
from accounts.models import AccountModel
from accounts.tests.utils.util import get_admin_payload, get_seller_payload
from categories.models import CategoryModel
from categorys.tests.utils import get_category_payload
from products.models import ProductModel
from rest_framework.test import APITestCase
from variations.models import VariationModel
from variations.tests.utils.gen_variation_functions import (
    get_product_payload, get_variation_payload)


class TestGetVariationById(APITestCase):
    PATH = "/products/variations/"

    @classmethod
    def setUpTestData(cls) -> None:
        cls.seller_data = get_seller_payload()
        cls.seller: AccountModel = AccountModel.objects.create_user(**cls.seller_data)

        cls.admin_data = get_admin_payload()
        cls.admin: AccountModel = AccountModel.objects.create_user(**cls.admin_data)
        
        cls.category_data = get_category_payload()
        cls.category: CategoryModel = CategoryModel.objects.create(**cls.category_data)

        # Creating store
        cls.store_data = get_store_payload()
        cls.store: StoreModel = StoreModel.objects.create(**cls.store_data)

        cls.product_data = get_product_payload()
        cls.product: ProductModel = ProductModel.objects.create(
            **cls.product_data, category_id=cls.category, store_id=cls.store
        )

        cls.variation_data = get_variation_payload()
        cls.variation: VariationModel = VariationModel.objects.create(**cls.variation_data, product_id=cls.product)
