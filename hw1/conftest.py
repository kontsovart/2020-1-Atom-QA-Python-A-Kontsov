import pytest
import random
import string


@pytest.fixture()
def generate_int_func():
    return random.randint(0, 100)


@pytest.fixture(scope='class')
def generate_int_class():
    return random.randint(101, 200)


@pytest.fixture(scope='session')
def generate_int_session():
    return random.randint(0, 100)


@pytest.fixture(autouse=True)
def random_list_ascii(generate_int_session):
    letters = string.ascii_lowercase
    list_ascii = []
    for i in range(generate_int_session):
        list_ascii.append(random.choice(letters))
    return list_ascii
