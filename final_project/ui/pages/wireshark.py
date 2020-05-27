from .base import BasePage
from ui.locators.locators import WiresharkPageLocators


class WiresharkPage(BasePage):
    locators = WiresharkPageLocators()
