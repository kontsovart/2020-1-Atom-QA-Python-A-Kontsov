import pytest

from api.mytarget_client import MyTargetClient
from ui.fixtures import *
import json


class TestMyTarget:

    @pytest.fixture(scope='function')
    def api_client(self):
        user = 'qa-python-target@yandex.ru'
        password = 'qazwsx123'

        return MyTargetClient(user, password)

    # @pytest.mark.skip(reason='TEMP')
    @pytest.mark.API
    def test_auth(self, api_client):
        api_client.auth_post()
        response = api_client.get_cabinet_page()
        api_client.get_z_cookie_page()
        assert 'qa-python-target@yandex.ru' in response.text

    # @pytest.mark.skip(reason='TEMP')
    @pytest.mark.API
    def test_new_segment(self, random_string_ascii, api_client):
        api_client.auth_post()
        api_client.get_base_csrf_token()
        api_client.get_z_cookie_page()
        api_client.get_segment_page()
        api_client.add_cookie(mc=api_client.session.cookies['mc'],
                              ssdc=api_client.session.cookies['ssdc'],
                              mrcu=api_client.session.cookies['mrcu'],
                              sdcs=api_client.session.cookies['sdcs'],
                              z_token=api_client.session.cookies['z'],
                              csrf_token=api_client.session.cookies['csrf_token'],
                              csrftoken=api_client.session.cookies['csrftoken'])
        response = api_client.add_segment_post(random_string_ascii)
        resp_json = response.json()
        assert random_string_ascii == resp_json['name']

    # @pytest.mark.skip(reason='TEMP')
    @pytest.mark.API
    def test_delete_segment(self, random_string_ascii, api_client):
        api_client.auth_post()
        api_client.get_base_csrf_token()
        api_client.get_z_cookie_page()
        api_client.get_segment_page()
        api_client.add_cookie(mc=api_client.session.cookies['mc'],
                              ssdc=api_client.session.cookies['ssdc'],
                              mrcu=api_client.session.cookies['mrcu'],
                              sdcs=api_client.session.cookies['sdcs'],
                              z_token=api_client.session.cookies['z'],
                              csrf_token=api_client.session.cookies['csrf_token'],
                              csrftoken=api_client.session.cookies['csrftoken'])
        response = api_client.add_segment_post(random_string_ascii)
        resp_json = response.json()
        response = api_client.delete_segment(segment_id=str(resp_json['id']))
        assert 204 == response.status_code

