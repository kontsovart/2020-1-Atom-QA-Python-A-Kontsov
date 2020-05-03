from mock.mock import users
import pytest
from socket_client.socket_client import HTTPClient
import json


def add_user(user_id: int, user_data: dict):
    users.update({str(user_id): user_data})


@pytest.mark.parametrize("users_id", [0, 1, 2])
def test_get_user(mock_server, users_id):
    server_host, server_port = mock_server
    client = HTTPClient(server_host, server_port)
    assert str(users_id) in json.loads(client.send_request_get(f"/user/{users_id}", json_bool=True))["data"]


@pytest.mark.parametrize("users_id", [0, 1, 2])
def test_delete_user(mock_server, users_id):
    server_host, server_port = mock_server
    client = HTTPClient(server_host, server_port)
    assert str(users_id) in json.loads(client.send_request_post(f"/user/delete?user_id={users_id}",
                                                                json_bool=True))["data"]
