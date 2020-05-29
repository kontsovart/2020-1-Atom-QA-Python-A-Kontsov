from urllib.parse import urljoin
import requests


class ResponseStatusCodeException(Exception):
    pass


class RequestErrorException(Exception):
    pass


class MailAppClient:

    def __init__(self, user, password, email, url):
        self.base_url = url

        self.session = requests.Session()

        self.user = user
        self.password = password
        self.email = email

    def get_welcome_page(self):
        location = 'welcome'
        return self.session.request('GET', urljoin(self.base_url, location))

    def get_find_me_error(self):
        location = 'static/scripts/findMeError.js'
        return self.session.request('GET', urljoin(self.base_url, location))

    def get_login_page(self):
        location = 'login'
        return self.session.request('GET', urljoin(self.base_url, location))

    def get_registration_page(self):
        location = 'reg'
        return self.session.request('GET', urljoin(self.base_url, location))

    def logout_get(self):
        location = 'logout'
        return self.session.request('GET', urljoin(self.base_url, location))

    def auth_post(self, confirm=None):
        location = 'login'
        data = {
            'username': self.user,
            'password': confirm if confirm else self.password,
            'submit': "Login"
        }
        return self.session.request('POST', urljoin(self.base_url, location), data=data)

    def registration_post(self, confirm=None, empty=False):
        location = 'reg'
        if empty:
            return self.session.request('POST', urljoin(self.base_url, location))
        data = {
            'username': self.user,
            'email': self.email,
            'password': self.password,
            'confirm': confirm if confirm else self.password,
            'term': 'y',
            'submit': "Login"
        }
        return self.session.request('POST', urljoin(self.base_url, location), data=data)

    def add_user_post(self, user=None, password=None, email=None, empty=False):
        location = 'api/add_user'
        if empty:
            return self.session.request('POST', urljoin(self.base_url, location))
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            'username': user,
            'password': password,
            'email': email
        }
        return self.session.request('POST', urljoin(self.base_url, location), headers=headers, json=data)

    def add_user_get(self):
        location = 'api/add_user'
        return self.session.request('GET', urljoin(self.base_url, location))

    def del_user_get(self, user=None, empty=False):
        if empty:
            location = f'api/del_user/'
        else:
            location = f'api/del_user/{user if user else self.user}'
        return self.session.request('GET', urljoin(self.base_url, location))

    def block_user_get(self, user=None, empty=False):
        if empty:
            location = f'api/block_user/'
        else:
            location = f'api/block_user/{user if user else self.user}'
        return self.session.request('GET', urljoin(self.base_url, location))

    def accept_user_get(self, user=None, empty=False):
        if empty:
            location = f'api/accept_user/'
        else:
            location = f'api/accept_user/{user if user else self.user}'
        return self.session.request('GET', urljoin(self.base_url, location))

    def status_app_get(self):
        location = f'status'
        return self.session.request('GET', urljoin(self.base_url, location))
