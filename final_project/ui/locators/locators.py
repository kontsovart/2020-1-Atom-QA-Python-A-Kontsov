from selenium.webdriver.common.by import By


class BaseLocators:
    pass


class MainPageLocators(BaseLocators):
    LOGIN_FRAME = (By.XPATH, '//div[@id="login-name"]//li[1]')
    VK_ID_FRAME = (By.XPATH, '//div[@id="login-name"]//li[2]')
    HOME_HREF = (By.XPATH, '//ul[@class="uk-navbar-nav uk-hidden-small"]//li[1]')
    PYTHON_HREF = (By.XPATH, '//a[@href="https://www.python.org/"]')
    WIKIPEDIA_HISTORY_HREF = (By.XPATH, '//a[@href="https://en.wikipedia.org/wiki/History_of_Python"]')
    FLASK_HREF = (By.XPATH, '//a[@href="https://flask.palletsprojects.com/en/1.1.x/#"]')
    LINUX_LI = (By.XPATH, '//ul[@class="uk-navbar-nav uk-hidden-small"]//li[3]')
    CENTOS_DOWNLOAD_HREF = (By.XPATH, '//a[@href="https://getfedora.org/ru/workstation/download/"]')
    NETWORK_LI = (By.XPATH, '//ul[@class="uk-navbar-nav uk-hidden-small"]//li[4]')
    WIRESHARK_NEWS_HREF = (By.XPATH, '//a[@href="https://www.wireshark.org/news/"]')
    WIRESHARK_DOWNLOAD_HREF = (By.XPATH, '//a[@href="https://www.wireshark.org/#download"]')
    TCP_DUMP_EXAMPLES = (By.XPATH, '//a[@href="https://hackertarget.com/tcpdump-examples/"]')
    WIKIPEDIA_API_HREF = (By.XPATH, '//a[@href="https://en.wikipedia.org/wiki/Application_programming_interface"]')
    POPULAR_MECHANIC_HREF = (By.XPATH, '//a[@href="https://www.popularmechanics.com/technology/'
                                       'infrastructure/a29666802/future-of-the-internet/"]')
    WIKIPEDIA_SMTP_HREF = (By.XPATH, '//a[@href="https://ru.wikipedia.org/wiki/SMTP"]')
    LOGOUT_BUTTON = (By.XPATH, '//a[@href="/logout"]')
    PYTHON_FACT_P = (By.XPATH, '//div[@class="uk-text-center uk-text-large"]//p[2]')
    TM_VERSION_BUTTON = (By.XPATH, '//a[@class="uk-navbar-brand uk-hidden-small"]')
    LINUX_HREF = (By.XPATH, '//ul[@class="uk-navbar-nav uk-hidden-small"]//li[3]//a')
    NETWORK_HREF = (By.XPATH, '//ul[@class="uk-navbar-nav uk-hidden-small"]//li[4]//a')


class LoginPageLocators(BaseLocators):
    LOGIN_INPUT = (By.XPATH,
                   '//input[@id="username"]')
    PASSWORD_INPUT = (By.XPATH,
                      '//input[@id="password"]')
    LOGIN_BUTTON = (By.XPATH,
                    '//input[@id="submit"]')
    FLASH_FRAME = (By.XPATH, '//div[@id="flash"]')
    REG_BUTTON = (By.XPATH, '//a[@href="/reg"]')
    FLASH_FRAME_STYLE = (By.XPATH, '//div[@id="flash"][contains(@style, "opacity: 0; visibility: hidden;")]')


class PythonPageLocators(BaseLocators):
    PYTHON_IMG = (By.XPATH, '//img[@class="python-logo"]')


class WikipediaPageLocators(BaseLocators):
    WIKIPEDIA_TITLE = (By.XPATH, '//h1[@id="firstHeading"]')


class FlaskPageLocators(BaseLocators):
    FLASK_IMG = (By.XPATH, '//img[@class="align-center"]')


class LinuxPageLocators(BaseLocators):
    FEDORA_IMG = (By.XPATH, '//img[@src="/static/images/fedora-logotext-white.png"]')


class WiresharkPageLocators(BaseLocators):
    GO_BEYOND_DIV = (By.XPATH, '//div[@class="ws-well-heading ws-well-heading-enhancement"]')
    DOWNLOAD_HEADER = (By.XPATH,
                       '//header[@class="text-center  element-normal-top element-no-bottom not-'
                       'condensed os-animation animated fadeInUp"]')


class TCPDumpPageLocators(BaseLocators):
    TCP_DUMP_EXAMPLE_H1 = (By.XPATH, '//h1[@class="btx-post-title post-title entry-title"]')


class PopularMechanicPageLocators(BaseLocators):
    INTERNET_HEADER_H1 = (By.XPATH, '//h1[@class="content-hed standard-hed"]')


class RegistrationPageLocators(BaseLocators):
    LOGIN_INPUT = (By.XPATH, '//input[@id="username"]')
    EMAIL_INPUT = (By.XPATH, '//input[@id="email"]')
    PASSWORD_INPUT = (By.XPATH, '//input[@id="password"]')
    CONFIRM_INPUT = (By.XPATH, '//input[@id="confirm"]')
    TERM_INPUT = (By.XPATH, '//input[@id="term"]')
    SUBMIT_BUTTON = (By.XPATH, '//input[@id="submit"]')
    FLASH_FRAME = (By.XPATH, '//div[@id="flash"]')
