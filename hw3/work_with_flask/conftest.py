import pytest
import requests

from mock import mock
from time import sleep

host = '127.0.0.1'
port = 5000
users = {0: ["abra", "cadabra"], 1: ["focus", "pocus"], 2: ["sim", "salabim"]}


@pytest.fixture(scope='session')
def mock_server():
    server = mock.run_mock(host, port)
    server_host = server._kwargs['host']
    server_port = server._kwargs['port']
    sleep(0.2)
    for user in users:
        user_add_url = f'http://{server_host}:{server_port}/user?' \
                       f'user_id={user}&' \
                       f'first_name={users[user][0]}&' \
                       f'last_name={users[user][0]}'
        requests.get(user_add_url)

    yield server_host, server_port

    shutdown_url = f'http://{server_host}:{server_port}/shutdown'
    requests.get(shutdown_url)
