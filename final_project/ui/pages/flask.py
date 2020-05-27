from .base import BasePage
from ui.locators.locators import FlaskPageLocators


class FlaskPage(BasePage):
    locators = FlaskPageLocators()
