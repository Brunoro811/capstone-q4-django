def variation_creation_model(product_instance):
    return {
        "size": "G",
        "quantity": 20,
        "color": "Verde",
        "product_id": product_instance,
    }


required_fields_in_response = [
    "id",
    "size",
    "quantity",
    "color",
    "is_active",
    "product_id",
]


def variation_update_route(product_id):
    return {
        "size": "M",
        "quantity": 30,
        "color": "Cinza",
        "product_id": product_id,
    }
