from .base import BasePage
from ui.locators.locators import LoginPageLocators
from selenium.webdriver.common.keys import Keys


class LoginPage(BasePage):
    locators = LoginPageLocators()

    def send_login_password(self, login, password):
        self.find(self.locators.LOGIN_INPUT).send_keys(login)
        self.find(self.locators.PASSWORD_INPUT).send_keys(password)
        self.click(self.locators.LOGIN_BUTTON)
