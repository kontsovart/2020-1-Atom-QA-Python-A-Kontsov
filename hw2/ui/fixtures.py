import pytest

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

from ui.pages.base import BasePage
from ui.pages.main import MainPage
from ui.pages.campaigns import CampaignsPage
from ui.pages.login import LoginPage
from ui.pages.audience import AudiencePage

import random
import string


class UsupportedBrowserException(Exception):
    pass


@pytest.fixture(scope='function')
def base_page(driver):
    return BasePage(driver)


@pytest.fixture(scope='function')
def main_page(driver):
    return MainPage(driver)


@pytest.fixture(scope='function')
def campaigns_page(driver):
    return CampaignsPage(driver)


@pytest.fixture(scope='function')
def login_page(driver):
    return LoginPage(driver)


@pytest.fixture(scope='function')
def audience_page(driver):
    return AudiencePage(driver)


@pytest.fixture(scope='function')
def driver(config):
    browser = config['browser']
    version = config['version']
    url = config['url']
    selenoid = config['selenoid']

    if browser == 'chrome' and selenoid == 'None':
        options = ChromeOptions()
        options.add_argument("--window-size=800,600")

        manager = ChromeDriverManager(version='latest')
        driver = webdriver.Chrome(executable_path=manager.install(),
                                  options=options,
                                  desired_capabilities={'acceptInsecureCerts': True}
                                  )

    elif selenoid != 'None':
        options = ChromeOptions()
        options.add_argument("--window-size=800,600")

        capabilities = {'acceptInsecureCerts': True,
                        'browserName': 'chrome',
                        'version': version,
                        }

        driver = webdriver.Remote(command_executor='http://' + selenoid + '/wd/hub/',
                                  options=options,
                                  desired_capabilities=capabilities
                                  )

    else:
        raise UsupportedBrowserException(f'Usupported browser: "{browser}"')

    driver.get(url)
    driver.maximize_window()
    yield driver
    driver.close()


@pytest.fixture(scope='function')
def get_campaigns_page(driver):
    return MainPage(driver).get_campaigns_page("qa-python-target@yandex.ru", "qazwsx123")


@pytest.fixture(scope='function')
def generate_int_function():
    return random.randint(0, 15)


@pytest.fixture(autouse=True)
def random_string_ascii(generate_int_function):
    letters = string.ascii_lowercase
    list_ascii = ""
    for i in range(generate_int_function):
        list_ascii += random.choice(letters)
    return list_ascii
