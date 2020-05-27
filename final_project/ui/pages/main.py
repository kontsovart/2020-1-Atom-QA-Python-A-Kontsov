from .base import BasePage
from ui.locators.locators import MainPageLocators
from selenium.webdriver import ActionChains


class MainPage(BasePage):
    locators = MainPageLocators()

    def go_to_home(self):
        self.click(self.locators.HOME_HREF)

    def go_to_python(self):
        self.click(self.locators.PYTHON_HREF)

    def go_to_wikipedia_history(self, ac):
        element = self.find(self.locators.PYTHON_HREF)
        ac.move_to_element(element).perform()
        self.click(self.locators.WIKIPEDIA_HISTORY_HREF)

    def go_to_flask(self, ac):
        windows_before = self.find_click_switch(find_locator=self.locators.PYTHON_HREF,
                                                click_locator=self.locators.FLASK_HREF,
                                                ac=ac)
        return windows_before

    def go_to_centos(self, ac):
        windows_before = self.find_click_switch(find_locator=self.locators.LINUX_LI,
                                                click_locator=self.locators.CENTOS_DOWNLOAD_HREF,
                                                ac=ac)
        return windows_before

    def go_to_wireshark_news(self, ac):
        windows_before = self.find_click_switch(find_locator=self.locators.NETWORK_LI,
                                                click_locator=self.locators.WIRESHARK_NEWS_HREF,
                                                ac=ac)
        return windows_before

    def go_to_wireshark_download(self, ac):
        windows_before = self.find_click_switch(find_locator=self.locators.NETWORK_LI,
                                                click_locator=self.locators.WIRESHARK_DOWNLOAD_HREF,
                                                ac=ac)
        return windows_before

    def go_to_tcp_dump_examples(self, ac):
        windows_before = self.find_click_switch(find_locator=self.locators.NETWORK_LI,
                                                click_locator=self.locators.TCP_DUMP_EXAMPLES,
                                                ac=ac)
        return windows_before

    def go_to_wikipedia_api(self, ac):
        windows_before = self.find_click_switch(find_locator=self.locators.WIKIPEDIA_API_HREF,
                                                click_locator=self.locators.WIKIPEDIA_API_HREF,
                                                ac=ac)
        return windows_before

    def go_to_popular_mechanic(self, ac):
        windows_before = self.find_click_switch(find_locator=self.locators.POPULAR_MECHANIC_HREF,
                                                click_locator=self.locators.POPULAR_MECHANIC_HREF,
                                                ac=ac)
        return windows_before

    def go_to_wikipedia_smtp(self, ac):
        windows_before = self.find_click_switch(find_locator=self.locators.WIKIPEDIA_SMTP_HREF,
                                                click_locator=self.locators.WIKIPEDIA_SMTP_HREF,
                                                ac=ac)
        return windows_before

    def find_click_switch(self, find_locator, click_locator, ac):
        element = self.find(find_locator)
        ac.move_to_element(element).perform()
        self.click(click_locator)
        self.wait_number_of_windows(number_win=2)
        windows_before = self.driver.current_window_handle
        windows_after = self.driver.window_handles
        new_window = [x for x in windows_after if x != windows_before][0]
        self.driver.switch_to.window(new_window)
        return windows_before

    def go_back(self, before_win):
        self.driver.close()
        self.driver.switch_to.window(before_win)
