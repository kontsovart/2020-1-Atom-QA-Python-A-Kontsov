from ui.fixtures import *

import pytest

from ui.pages.base import BasePage
from ui.pages.main import MainPage
from ui.pages.login import LoginPage
from ui.pages.python import PythonPage
from ui.pages.wikipedia import WikipediaPage
from ui.pages.flask import FlaskPage
from ui.pages.linux import LinuxPage
from ui.pages.wireshark import WiresharkPage
from ui.pages.popularmechanic import PopularMechanicPage
from ui.pages.tcpdump import TCPDumpPage
from ui.pages.registration import RegistrationPage


class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request):
        self.driver = driver
        self.config = config
        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.main_page: MainPage = request.getfixturevalue('main_page')
        self.login_page: LoginPage = request.getfixturevalue('login_page')
        self.python_page: PythonPage = request.getfixturevalue('python_page')
        self.wikipedia_page: WikipediaPage = request.getfixturevalue('wikipedia_page')
        self.flask_page: FlaskPage = request.getfixturevalue('flask_page')
        self.linux_page: LinuxPage = request.getfixturevalue('linux_page')
        self.wireshark_page: WiresharkPage = request.getfixturevalue('wireshark_page')
        self.tcp_dump_page: TCPDumpPage = request.getfixturevalue('tcp_dump_page')
        self.popular_mechanic_page: PopularMechanicPage = request.getfixturevalue('popular_mechanic_page')
        self.registration_page: RegistrationPage = request.getfixturevalue('registration_page')
