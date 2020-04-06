from ui.fixtures import *

import pytest
import os

from ui.pages.base import BasePage
from ui.pages.main import MainPage
from ui.pages.campaigns import CampaignsPage
from ui.pages.login import LoginPage
from ui.pages.audience import AudiencePage
from ui.decorators import wait


class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request):
        self.driver = driver
        self.config = config
        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.main_page: MainPage = request.getfixturevalue('main_page')
        self.campaigns_page: CampaignsPage = request.getfixturevalue('campaigns_page')
        self.login_page: LoginPage = request.getfixturevalue('login_page')
        self.audience_page: AudiencePage = request.getfixturevalue('audience_page')
