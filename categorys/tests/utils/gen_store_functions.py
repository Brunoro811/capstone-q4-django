from faker import Faker

fake = Faker()


def get_category_payload():
    return {
        "name": fake.unique.word()
    }
