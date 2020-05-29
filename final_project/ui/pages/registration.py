from .base import BasePage
from ui.locators.locators import RegistrationPageLocators


class RegistrationPage(BasePage):
    locators = RegistrationPageLocators()

    def registration(self, user_data):
        self.click(self.locators.LOGIN_INPUT).send_keys(user_data["username"])
        self.click(self.locators.EMAIL_INPUT).send_keys(user_data["email"])
        self.click(self.locators.PASSWORD_INPUT).send_keys(user_data["password"])
        self.click(self.locators.CONFIRM_INPUT).send_keys(user_data.get("confirm", user_data["password"]))
        self.click(self.locators.TERM_INPUT)
        self.click(self.locators.SUBMIT_BUTTON)
