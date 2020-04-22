from .base import BasePage
from .campaigns import CampaignsPage
from ui.locators.locators import MainPageLocators
from .login import LoginPage


class MainPage(BasePage):
    locators = MainPageLocators()

    def go_to_campaigns(self):
        self.click(self.locators.ENTER_TO_CABINET)
        return CampaignsPage(self.driver)

    def go_to_login(self):
        self.click(self.locators.ENTER_TO_CABINET)
        return LoginPage(self.driver)

    def send_login_password(self, login, password):
        self.click(self.locators.AUTHORIZATION, timeout=12)
        self.find(self.locators.LOGIN_FRAME)
        self.find(self.locators.LOGIN_INPUT).send_keys(login)
        self.find(self.locators.PASSWORD_INPUT).send_keys(password)

    def get_campaigns_page(self, login, password):
        self.send_login_password(login, password)
        return self.go_to_campaigns()
