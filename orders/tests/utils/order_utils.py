import random
from functools import reduce

from faker import Faker

fake = Faker()
from orders.models import OrdersModel, OrderVariationsModel


def variation_request(variation_list: list):
    return {
        "variations": [
            {"id": str(variation.id), "quantity": variation.quantity}
            for variation in variation_list
        ]
    }


def variation_creation_model(product_id):
    return {
        "size": random.choice("PMG"),
        "quantity": random.randint(0, 200),
        "color": fake.color_name(),
        "product_id": product_id,
    }


fields_in_response = [
    "id",
    "created_at",
    "total_value",
    "seller_id",
    "store_id",
    "products",
]

fields_in_products_in_response = ["product", "sale_value", "quantity"]
fields_in_each_product_in_response = [
    "id",
    "name",
    "cost_value",
    "sale_value_retail",
    "sale_value_wholesale",
    "quantity_wholesale",
    "store_id",
    "category",
    "variation",
]
fields_in_variation_product = [
    "id",
    "size",
    "color",
    "product_id",
    "is_active",
    "quantity",
]


def order_and_order_variations(variations, seller_id, store_id):

    order_variations = [
        OrderVariationsModel(
            {
                # define se o preço será de atacado ou varejo baseado na quantidade mínima para tal
                "sale_value": variation.product_id.sale_value_wholesale
                if variation.quantity >= variation.product_id.quantity_wholesale
                else variation.product_id.sale_value_retail,
                "quantity": variation.quantity,
                "order_id": str(order.id),
                "variation_id": str(variation.id),
            }
        )
        for variation in variations
    ]

    order_variations_instances = OrderVariationsModel.objects.bulk_create(
        order_variations
    )

    order = OrdersModel.objects.create(
        total_value=reduce(
            lambda a, b: a + b,
            [
                variation.sale_value * variation.quantity
                for variation in order_variations
            ],
        ),
        seller_id=seller_id,
        store_id=store_id,
    )

    return order, order_variations_instances
