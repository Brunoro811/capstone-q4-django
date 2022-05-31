from faker import Faker

fake = Faker()


def get_variation_payload():
    return {
        "size": "M",
        "quantity": fake.random_number(2),
        "color": fake.color_name(),
    }


def get_product_payload():
    return {
        "name": fake.unique.word(),
        "cost_value": fake.random_number(2),
        "sale_value_retail": fake.random_number(2),
        "sale_value_wholesale": fake.random_number(2),
        "quantity_wholesale": fake.random_number(2),
    }
