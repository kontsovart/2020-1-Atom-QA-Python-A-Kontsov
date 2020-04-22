from .base import BasePage
from ui.locators.locators import LoginPageLocators
from selenium.webdriver.common.keys import Keys


class LoginPage(BasePage):
    locators = LoginPageLocators()
