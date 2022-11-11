import datetime
import random

from faker import Faker


def generate_random_date():
    """generates mature users birth date"""
    faker = Faker()
    Faker.seed(0)
    return faker.date_between_dates(datetime.date(1900, 1, 1), datetime.date(2004, 11, 1))


def random_role_id():
    return random.randint(0, 1)
