from faker import Faker

fake = Faker()


store_correct = {
    'name': fake.company(),
    'street': fake.street_name(),
    'number': fake.building_number(),
    'state': fake.current_country_code(),
    'other_information': '',
    'zip_code': fake.postcode(),
}
