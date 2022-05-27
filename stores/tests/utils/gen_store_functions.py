from faker import Faker

fake = Faker()


def get_store_payload():
    return {
        "name": fake.unique.company(),
        "state": fake.state(),
        "street": fake.street_name(),
        "number": fake.numerify(),
        "zip_code": fake.zipcode(),
        "other_information": fake.text(150),
    }
