from .base import BasePage
from ui.locators.locators import CampaignsPageLocators
from .audience import AudiencePage
from selenium.common.exceptions import TimeoutException
from ui.decorators import passage
import os


class LackOfButtonCreateCampaign(Exception):
    pass


class CampaignsPage(BasePage):
    locators = CampaignsPageLocators()

    def go_to_audience(self):
        self.click(self.locators.AUDIENCE_PAGE)
        return AudiencePage(self.driver)

    def create_new_campaign_click(self):
        check_create = False
        try:
            self.click(self.locators.CAMPAIGNS_NEW)
            check_create = True
        except TimeoutException:
            pass
        if check_create is False:
            try:
                self.click(self.locators.CREATE_CAMPAIGN_MAIN)
            except TimeoutException:
                raise LackOfButtonCreateCampaign

    def active_traffic_item_click(self, ac):
        element = self.find(self.locators.ACTIVE_TRAFFIC_ITEM)
        ac.move_to_element(element).perform()
        self.click(self.locators.ACTIVE_TRAFFIC_ITEM)

    def send_keys_to_link(self, ac, link):
        element = self.find(self.locators.INPUT_LINK_FIELD)
        ac.move_to_element(element).perform()
        self.click(self.locators.INPUT_LINK_FIELD).send_keys(link)

    def send_keys_to_name(self, name):
        self.scroll_to_element(self.driver.find_element(*self.locators.INPUT_NAME_FIELD))
        self.click(self.locators.INPUT_NAME_FIELD).clear()
        self.click(self.locators.INPUT_NAME_FIELD).send_keys(name)

    def banner_slot_click(self):
        self.find(self.locators.BANNER_SLOT)
        self.click(self.locators.BANNER_SLOT)

    def upload_image(self, ac, image_name):
        element = self.find(self.locators.UPLOAD_IMAGE_BUTTON)
        self.scroll_to_element(self.driver.find_element(*self.locators.UPLOAD_IMAGE_BUTTON))
        ac.move_to_element(element).perform()
        self.find(self.locators.UPLOAD_IMAGE).send_keys(
            *passage(image_name, os.getcwd()))

    def submit_advertisement_click(self):
        self.find(self.locators.SUBMIT_ADVERTISEMENT)
        self.click(self.locators.SUBMIT_ADVERTISEMENT)

    def save_button_click(self):
        self.find(self.locators.SAVE_BUTTON)
        self.click(self.locators.SAVE_BUTTON)
