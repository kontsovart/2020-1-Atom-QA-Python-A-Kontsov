import pytest

from api.mytarget_client import MyTargetClient
from ui.fixtures import *


class TestMyTarget:

    @pytest.fixture(scope='session')
    def api_client(self):
        user = 'qa-python-target@yandex.ru'
        password = 'qazwsx123'

        return MyTargetClient(user, password)

    @pytest.mark.API
    def test_auth(self, api_client):
        response = api_client.get_cabinet_page()
        assert 'qa-python-target@yandex.ru' in response.text

    @pytest.mark.API
    def test_new_segment(self, random_string_ascii, api_client):
        response = api_client.add_segment_post(random_string_ascii)
        resp_json = response.json()
        assert random_string_ascii == resp_json['name']

    @pytest.mark.API
    def test_delete_segment(self, random_string_ascii, api_client):
        response = api_client.add_segment_post(random_string_ascii)
        resp_json = response.json()
        response = api_client.delete_segment(segment_id=str(resp_json['id']))
        assert 204 == response.status_code
