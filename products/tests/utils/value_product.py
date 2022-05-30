from categorys.models import CategoryModel
from stores.models import StoreModel


def product_shirt ():

    """
        This function return dict shirt with `category_id`  and `store_id` empty.
    """

    return {
        'name': 'Camiseta Casual',
        'cost_value': 15.99,
        'sale_value_retail': 46.99,
        'sale_value_wholesale': 35.99,
        'store_id': StoreModel.objects.all()[0] ,
        'category_id': StoreModel.objects.all()[0],
        'quantity_wholesale': 10,
    }
