from faker import Faker
from faker.providers.person import Provider

fake = Faker()

fake.add_provider(Provider)
fake: Provider


def user_admin_correct():
    return {
        "username": fake.unique.user_name(),
        "email": fake.unique.email(),
        "password": fake.password(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "is_admin": True,
        "is_seller": True,
}

user_admin_incorrect_email = {
    "username": fake.unique.user_name(),
    "email": fake.unique.email(),
    "password": fake.password(),
    "first_name": fake.first_name(),
    "last_name": fake.last_name(),
    "is_admin": True,
    "is_seller": True,
}

def user_seller_correct():
    return {
    'username': fake.unique.user_name(),
    'email': fake.unique.email(),
    'password': fake.password(),
    'first_name': fake.first_name(),
    'last_name': fake.last_name(),
    'is_admin': False,
    'is_seller': True

    }

user_seller_incorrect_email = {
    "username": fake.user_name(),
    "email": fake.email(),
    "password": fake.password(),
    "first_name": fake.first_name(),
    "last_name": fake.last_name(),
    "is_admin": False,
    "is_seller": True,
}

unauthorized_details = {"detail": "Authentication credentials were not provided."}

forbidden_details = {"detail": "You do not have permission to perform this action."}

username_conflict_detail = {"username": ["user with this username already exists."]}

email_conflict_detail = {"email": ["user with this email already exists."]}

create_account_201_response_fields = (
    "id",
    "username",
    "is_admin",
    "is_seller",
    "email",
    "first_name",
    "last_name",
    "created_at",
    "store_id",
)


def get_admin_payload():
    return {
        "username": fake.unique.user_name(),
        "email": fake.unique.email(),
        "password": fake.password(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "is_admin": True,
        "is_seller": True,
    }


def get_seller_payload():
    return {
        "username": fake.unique.user_name(),
        "email": fake.unique.email(),
        "password": fake.password(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "is_admin": False,
        "is_seller": True,
    }
