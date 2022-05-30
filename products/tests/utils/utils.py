def correct_product(store, category):
    return {
        "name": "Botas muito boas",
        "cost_value": 19.99,
        "sale_value_retail": 18.99,
        "sale_value_wholesale": 16.99,
        "quantity_wholesale": 200,
        "store_id": store,
        "category_id": category,
    }


def product_update(store_id, category):
    return {
        "name": "Botas muito boas melhores ainda",
        "cost_value": 29.99,
        "sale_value_retail": 28.99,
        "sale_value_wholesale": 26.99,
        "quantity_wholesale": 400,
        "store_id": store_id,
        "category_id": category,
    }


products_fields_response = [
    "name",
    "cost_value",
    "sale_value_retail",
    "sale_value_wholesale",
    "quantity_wholesale",
    "store_id",
    "category_id",
]
