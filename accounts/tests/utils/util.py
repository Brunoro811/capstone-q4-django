from faker import Faker
from faker.providers.person import Provider

fake = Faker()

fake.add_provider(Provider)
fake : Provider

user_admin_correct = {
    'email': fake.email(),
    'password': fake.password(),
    'first_name': fake.first_name(),
    'last_name': fake.last_name(),
    'is_admin': True,
    'is_seller': True
}

user_admin_incorrect_email = {
    'email': fake.email().replace('@',''),
    'password': fake.password(),
    'first_name': fake.first_name(),
    'last_name': fake.last_name(),
    'is_admin': True,
    'is_seller': True
}

user_seller_correct = {
    'email': fake.email(),
    'password': fake.password(),
    'first_name': fake.first_name(),
    'last_name': fake.last_name(),
    'is_admin': False,
    'is_seller': True
}

user_seller_incorrect_email = {
    'email': fake.email().replace('@',''),
    'password': fake.password(),
    'first_name': fake.first_name(),
    'last_name': fake.last_name(),
    'is_admin': False,
    'is_seller': True
}
