import random

from faker import Faker

fake = Faker()


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
fields_in_variation_product = ["id", "size", "color", "product_id"]
def order_creation_model():
    return {
        
    }