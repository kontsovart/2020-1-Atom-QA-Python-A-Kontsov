from urllib.parse import urljoin
from http.cookies import SimpleCookie
import json

import requests
from requests.cookies import cookiejar_from_dict


class ResponseStatusCodeException(Exception):
    pass


class RequestErrorException(Exception):
    pass


class MyTargetClient:

    def __init__(self, user, password):
        self.base_url = 'https://target.my.com'
        self.auth_url = 'https://auth-ac.my.com/auth?lang=ru&nosavelogin=0'
        self.login_url = 'https://account.my.com/login/'
        self.csrf_url = 'https://target.my.com/csrf/'
        self.campaigns_url = 'https://target.my.com/campaigns/list'
        self.segment_url = 'https://target.my.com/segments/segments_list'
        self.cookie_z_url = 'https://target.my.com/api/v2/localization_components.json?lang=en,ru'

        self.session = requests.Session()

        self.user = user
        self.password = password

    def get_auth_csrf_token(self):
        response = self.session.request('GET', self.login_url)
        set_cookie = response.headers['Set-Cookie'].split(';')
        new_csrf_token = [c for c in set_cookie if c.startswith('csrf_token=')][0].split('=')[-1]
        self.csrf_token = new_csrf_token

    def get_base_csrf_token(self):
        response = self.session.request('GET', self.csrf_url)
        set_cookie = response.headers['Set-Cookie'].split(';')
        new_csrf_token = [c for c in set_cookie if c.startswith('csrftoken=')][0].split('=')[-1]
        self.csrf_token = new_csrf_token

    def get_cabinet_page(self):
        location = 'campaigns/list'
        return self.session.request('GET', urljoin(self.base_url, location))

    def get_segment_page(self):
        location = 'segments'
        return self.session.request('GET', urljoin(self.base_url, location))

    def get_z_cookie_page(self):
        return self.session.request('GET', self.cookie_z_url)

    def auth_post(self):
        self.get_auth_csrf_token()
        self.session.request('GET', self.base_url)
        headers = {
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;'
                       'q=0.8,application/signed-exchange;v=b3;q=0.9',
             'Accept-Encoding': 'gzip, deflate, br',
             'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
             'Cache-Control': 'max-age=0',
             'Connection': 'keep-alive',

             'Content-Type': 'application/x-www-form-urlencoded',
             'Host': 'auth-ac.my.com',
             'Origin': 'https://target.my.com',
             'Referer': 'https://target.my.com/',
             'Sec-Fetch-Dest': 'document',
             'Sec-Fetch-Mode': 'navigate',
             'Sec-Fetch-Site': 'same-site',
             'Sec-Fetch-User': '?1',
             'Upgrade-Insecure-Requests': '1',
             'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/80.0.3987.162 Safari/537.36'
        }

        data = {
            'email': self.user,
            'password': self.password,
            'continue': 'https://target.my.com/auth/mycom?state=target_login%3D1#email',
            'failure': 'https://account.my.com/login/'
        }
        return self.session.request('POST', self.auth_url, data=data, headers=headers, allow_redirects=False)

    def add_cookie(self, mc, ssdc, mrcu, sdcs, z_token, csrf_token, csrftoken):
        self.mc_token = mc
        self.ssdc_token = ssdc
        self.mrcu_token = mrcu
        self.sdcs_token = sdcs
        self.z_token = z_token
        self.csrf_token = csrf_token
        self.csrftoken = csrftoken

    def add_segment_post(self, segment_name):
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru',
            'Connection': 'keep-alive',

            'Content-Type': 'application/json',
            'DNT': '1',
            'Host': 'target.my.com',
            'Origin': 'https://target.my.com',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Referer': 'https://target.my.com/segments/segments_list/new',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/80.0.3987.162 Safari/537.36',
            'X-CSRFToken': self.session.cookies['csrftoken'],
            'X-Requested-With': 'XMLHttpRequest'
        }
        location = 'api/v2/remarketing/segments.json?fields=relations__object_type,relations__object_id,' \
                   'relations__params,relations_count,id,name,pass_condition,created,campaign_ids,users,flags'
        data = {"name": segment_name,
                "pass_condition": 1,
                "relations": [
                    {"object_type": "remarketing_player",
                     "params":
                         {"type": "positive",
                          "left": 365,
                          "right": 0
                          }
                     }
                ],
                "logicType": "or"}
        response = self.session.request("POST", urljoin(self.base_url, location), headers=headers, json=data)
        return response
