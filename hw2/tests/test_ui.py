import pytest
from selenium.webdriver import ActionChains
from tests.base_ui import BaseCase


class Test(BaseCase):

    # @pytest.mark.skip(reason='TEMP')
    @pytest.mark.UI
    def test_auth_positive(self):
        self.main_page.send_login_password("qa-python-target@yandex.ru", "qazwsx123")
        campaigns_page = self.main_page.go_to_campaigns()
        element = campaigns_page.find(self.campaigns_page.locators.USERNAME_WRAP)
        assert "qa-python-target@yandex.ru" in element.text.lower()

    # @pytest.mark.skip(reason='TEMP')
    @pytest.mark.UI
    def test_auth_negative(self):
        self.main_page.send_login_password("123", "123")
        login_page = self.main_page.go_to_login()
        element = login_page.find(self.login_page.locators.INVALID_LOGIN_OR_PASSWORD)
        assert 'Invalid login or password' in element.text

    # @pytest.mark.skip(reason='TEMP')
    @pytest.mark.UI
    def test_auth_fixture(self, get_campaigns_page):
        element = get_campaigns_page.find(self.campaigns_page.locators.USERNAME_WRAP)
        assert "qa-python-target@yandex.ru" in element.text.lower()

    # @pytest.mark.skip(reason='TEMP')
    @pytest.mark.UI
    def test_new_campaign(self, random_string_ascii):
        self.main_page.send_login_password("qa-python-target@yandex.ru", "qazwsx123")
        campaigns_page = self.main_page.go_to_campaigns()

        campaigns_page.create_new_campaign_click()

        ac = ActionChains(self.driver)

        campaigns_page.active_traffic_item_click(ac=ac)
        campaigns_page.send_keys_to_link(ac=ac, link="https://target.my.com")
        campaigns_page.send_keys_to_name(name=random_string_ascii)
        campaigns_page.banner_slot_click()
        campaigns_page.upload_image(ac=ac, image_name='62144605.jpg')
        campaigns_page.submit_advertisement_click()
        campaigns_page.save_button_click()
        element = campaigns_page.find(self.campaigns_page.locators.LAST_CAMPAIGN_NAME)
        assert random_string_ascii in element.text

    # @pytest.mark.skip(reason='TEMP')
    @pytest.mark.UI
    def test_new_audience(self, random_string_ascii):
        self.main_page.send_login_password("qa-python-target@yandex.ru", "qazwsx123")
        campaigns_page = self.main_page.go_to_campaigns()
        audience_page = campaigns_page.go_to_audience()

        audience_page.create_new_audience_click()

        ac = ActionChains(self.driver)

        audience_page.add_segment_window(ac)
        audience_page.input_segment_name(random_string_ascii)
        audience_page.submit_all_segment_click()

        element = audience_page.find(self.audience_page.locators.SEGMENT_NAME)
        assert random_string_ascii in element.get_attribute("title")

    # @pytest.mark.skip(reason='TEMP')
    @pytest.mark.UI
    def test_delete_audience(self, random_string_ascii):
        self.main_page.send_login_password("qa-python-target@yandex.ru", "qazwsx123")
        campaigns_page = self.main_page.go_to_campaigns()
        audience_page = campaigns_page.go_to_audience()

        audience_page.create_new_audience_click()
        ac = ActionChains(self.driver)
        audience_page.add_segment_window(ac)
        audience_page.input_segment_name(random_string_ascii)
        audience_page.submit_all_segment_click()

        audience_page.delete_segment()
