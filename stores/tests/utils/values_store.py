from datetime import datetime

from faker import Faker

fake = Faker()


store_correct = {
    'name': fake.company(),
    'street': fake.street_name(),
    'number': fake.building_number(),
    'state': fake.current_country_code(),
    'other_information': '',
    'zip_code': fake.postcode(),
    'updated_at': datetime.utcnow()
}

get_store_by_id_200_response_fields = [
    "id",
    "name",
    "state",
    "street",
    "number",
    "zip_code",
    "is_active",
    "other_information",
    "created_at",
    "updated_at",
    "sellers",
    "admins"
]
