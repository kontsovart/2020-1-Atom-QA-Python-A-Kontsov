from ui.fixtures import *
from base.mysql_orm_client.mysql_orm_client import MysqlOrmConnection
from base.builder.orm_builder import MysqlOrmBuilder
import requests
import random
import string
from urllib.parse import urljoin

import pytest


class UsupportedBrowserException(Exception):
    pass


def pytest_addoption(parser):
    parser.addoption('--url_app', default='http://localhost:12345/')
    parser.addoption('--url_app_selenoid', default='http://my_app_container:12345/')
    parser.addoption('--url_vk_api', default='http://localhost:5000/')
    parser.addoption('--db_host', default='localhost')
    parser.addoption('--db_port', default=3306)
    parser.addoption('--database_name', default='mail_app')
    parser.addoption('--db_user', default='test_qa')
    parser.addoption('--db_user_password', default='qa_test')
    parser.addoption('--browser', default='chrome')
    parser.addoption('--browser_ver', default='80.0')
    parser.addoption('--selenoid', default=None)


@pytest.fixture(scope='session')
def config(request):
    url_app = request.config.getoption('--url_app')
    url_app_selenoid = request.config.getoption('--url_app_selenoid')
    url_vk_api = request.config.getoption('--url_vk_api')
    db_host = request.config.getoption('--db_host')
    db_port = request.config.getoption('--db_port')
    database_name = request.config.getoption('--database_name')
    db_user = request.config.getoption('--db_user')
    db_user_password = request.config.getoption('--db_user_password')
    browser = request.config.getoption('--browser')
    version = request.config.getoption('--browser_ver')
    selenoid = request.config.getoption('--selenoid')

    return {'browser': browser,
            'version': version,
            'url_app': url_app,
            'url_app_selenoid': url_app_selenoid,
            'url_vk_api': url_vk_api,
            'db_host': db_host,
            'db_port': db_port,
            'db_name': database_name,
            'db_user': db_user,
            'db_user_password': db_user_password,
            'selenoid': selenoid}


def pytest_configure(config):
    db_connector = MysqlOrmConnection(user=config.getoption('--db_user'),
                                      password=config.getoption('--db_user_password'),
                                      db_name=config.getoption('--database_name'),
                                      host=config.getoption('--db_host'),
                                      port=config.getoption('--db_port'))
    config.db_connector = db_connector
    if not hasattr(config, 'slaveinput'):
        db_builder = MysqlOrmBuilder(db_connector)
        config.db_builder = db_builder
        config.db_builder.create_test_users()


@pytest.fixture(scope='function')
def generate_int_function():
    return random.randint(6, 15)


@pytest.fixture(scope='function')
def random_string_ascii(generate_int_function):
    letters = string.ascii_lowercase
    digits = string.digits
    list_ascii = ""
    for i in range(generate_int_function):
        list_ascii += random.choice(letters + digits)
    return list_ascii


@pytest.fixture(scope='function')
def random_user(generate_int_function, random_string_ascii):
    username = random_string_ascii
    password = random_string_ascii
    email = random_string_ascii + "@yandex.ru"
    vk_id = generate_int_function
    return {"username": username, "password": password, "email": email, "vk_id": vk_id}


@pytest.fixture(scope='session')
def setup_base(request):
    mysql: MysqlOrmConnection = request.config.db_connector
    builder = MysqlOrmBuilder(mysql)
    return mysql, builder


@pytest.fixture(scope='session')
def generate_int_session():
    return random.randint(6, 15)


@pytest.fixture(scope='session')
def random_string_session(generate_int_session):
    letters = string.ascii_lowercase
    digits = string.digits
    list_ascii = ""
    for i in range(generate_int_session):
        list_ascii += random.choice(letters + digits)
    return list_ascii


@pytest.fixture(scope='session')
def stable_user(setup_base, random_string_session, generate_int_session, config):
    mysql, builder = setup_base

    username = random_string_session
    password = random_string_session
    email = random_string_session + "@yandex.ru"
    vk_id = str(generate_int_session)

    user = builder.add_user(username=username,
                            password=password,
                            email=email,
                            access=1,
                            active=0,
                            start_active_time=None)
    vk_api_url = config['url_vk_api']
    requests.get(urljoin(vk_api_url, f"/vk_id/add?username={username}&vk_id={vk_id}"))
    return {"username": username, "password": password, "email": email, "vk_id": vk_id}, user.id
