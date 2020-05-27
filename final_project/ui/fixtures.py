import pytest

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from ui.pages.base import BasePage
from ui.pages.main import MainPage
from ui.pages.login import LoginPage
from ui.pages.python import PythonPage
from ui.pages.wikipedia import WikipediaPage
from ui.pages.flask import FlaskPage
from ui.pages.linux import LinuxPage
from ui.pages.wireshark import WiresharkPage
from ui.pages.tcpdump import TCPDumpPage
from ui.pages.popularmechanic import PopularMechanicPage
from ui.pages.registration import RegistrationPage

import allure
import subprocess


class UsupportedBrowserException(Exception):
    pass


@pytest.fixture(scope='function')
def base_page(driver):
    return BasePage(driver)


@pytest.fixture(scope='function')
def main_page(driver):
    return MainPage(driver)


@pytest.fixture(scope='function')
def login_page(driver):
    return LoginPage(driver)


@pytest.fixture(scope='function')
def python_page(driver):
    return PythonPage(driver)


@pytest.fixture(scope='function')
def wikipedia_page(driver):
    return WikipediaPage(driver)


@pytest.fixture(scope='function')
def flask_page(driver):
    return FlaskPage(driver)


@pytest.fixture(scope='function')
def linux_page(driver):
    return LinuxPage(driver)


@pytest.fixture(scope='function')
def wireshark_page(driver):
    return WiresharkPage(driver)


@pytest.fixture(scope='function')
def tcp_dump_page(driver):
    return TCPDumpPage(driver)


@pytest.fixture(scope='function')
def popular_mechanic_page(driver):
    return PopularMechanicPage(driver)


@pytest.fixture(scope='function')
def registration_page(driver):
    return RegistrationPage(driver)


@pytest.fixture(scope='function')
def driver(config):
    browser = config['browser']
    version = config['version']
    url = config['url_app']
    url_selenoid = config['url_app_selenoid']
    selenoid = config['selenoid']

    if browser == 'chrome' and selenoid is None:

        manager = ChromeDriverManager(version='latest')
        driver = webdriver.Chrome(executable_path=manager.install(),
                                  desired_capabilities={'acceptInsecureCerts': True}
                                  )
        driver.get(url)
    elif selenoid is not None:
        capabilities = {'acceptInsecureCerts': True,
                        'browserName': 'chrome',
                        'version': version,
                        }

        driver = webdriver.Remote(command_executor='http://' + selenoid + '/wd/hub/',
                                  desired_capabilities=capabilities
                                  )
        driver.get(url_selenoid)
    else:
        raise UsupportedBrowserException(f'Usupported browser: "{browser}"')

    driver.maximize_window()
    yield driver
    driver.close()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture(scope="function")
def take_screenshot_when_failure(request, driver):
    yield
    if request.node.rep_call.failed:
        allure.attach('\n'.join(driver.get_log('browser')),
                      name='console.log',
                      attachment_type=allure.attachment_type.TEXT)
        allure.attach(driver.get_screenshot_as_png(),
                      name=request.node.location[-1],
                      attachment_type=allure.attachment_type.PNG)


@pytest.fixture(scope="function")
def take_logs_when_failure(request):
    yield
    if request.node.rep_call.failed:
        allure.attach(subprocess.check_output("docker logs my_app_container", shell=True),
                      name='console.log',
                      attachment_type=allure.attachment_type.TEXT)
