from datetime import datetime

from faker import Faker

fake = Faker()


store_correct = {
    "name": fake.company(),
    "street": fake.street_name(),
    "number": fake.building_number(),
    "state": fake.current_country_code(),
    "other_information": "",
    "zip_code": fake.postcode(),
}

store_success = {
    "name": "Empresa limitada",
    "street": "rua tal",
    "number": 555,
    "state": "MG",
    "other_information": "Nã é fantasma",
    "zip_code": "99999999",
}

fields_response_create_store = [
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
]

fields_request_create_store = [
    "name",
    "street",
    "number",
    "state",
    "other_information",
    "zip_code",
]

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
    "admins",
]

store_success_update = {
    "name": "Empresa limitada version7.0",
    "street": "rua tal esquina tal",
    "number": 456,
    "state": "ES",
    "other_information": "Não existe sequer a possibilidade de essa empresa ser uma empresa fantasma",
    "zip_code": "88888888",
}
