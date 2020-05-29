import pytest
from selenium.webdriver import ActionChains
from tests.base_ui import BaseCase


class Test(BaseCase):

    @pytest.mark.usefixtures("take_screenshot_when_failure")
    @pytest.mark.UI
    def test_auth_positive(self, stable_user):
        """Тест проверяет успешную авторизацию.

        Стабильный пользователь авторизуется, проверяется наличие формы с именем
        пользователя на главной странице.
        """
        user, _ = stable_user
        self.login_page.send_login_password(user["username"], user["password"])
        element = self.main_page.find(self.main_page.locators.LOGIN_FRAME)
        assert user["username"] in element.text.lower()

    @pytest.mark.parametrize("user_pass", [["123123", "123"],
                                           ["123", "123"],
                                           ["2"*17, "123"],
                                           ["321456", "1"*256]])
    @pytest.mark.usefixtures("take_screenshot_when_failure")
    @pytest.mark.UI
    def test_auth_negative(self, user_pass):
        """Тест проверяет негативную авторизацию.

        Проверяются случаи:
        1) остуствие пользователя в базе данных
        2), 3) некорректная длина имени пользователя
        4) некорректная длина пароля.
        Проверяется текст всплывающего уведомления.
        """
        self.login_page.send_login_password(user_pass[0], user_pass[1])
        element = self.login_page.find(self.login_page.locators.FLASH_FRAME)
        assert element.get_attribute("textContent").lower() in ["invalid username or password",
                                                                "incorrect username length"]

    @pytest.mark.usefixtures("take_screenshot_when_failure")
    @pytest.mark.UI
    def test_auth_negative_user(self, stable_user):
        """Тест проверяет негативную авторизацию.

       Проверяется случай пустого окна с именем пользователя.
       """
        user, _ = stable_user
        self.login_page.send_login_password("", user["password"])
        self.login_page.find(self.login_page.locators.LOGIN_BUTTON)

    @pytest.mark.usefixtures("take_screenshot_when_failure")
    @pytest.mark.UI
    def test_auth_negative_password(self, stable_user):
        """Тест проверяет негативную авторизацию.

       Проверяется случай пустого окна с паролем.
       """
        user, _ = stable_user
        self.login_page.send_login_password(user["username"], "")
        self.login_page.find(self.login_page.locators.LOGIN_BUTTON)

    @pytest.mark.usefixtures("take_screenshot_when_failure")
    @pytest.mark.UI
    def test_auth_negative_all(self):
        """Тест проверяет негативную авторизацию.

       Проверяется случай пустого окна с именем пользователя и пустого окна с паролем.
       """
        self.login_page.send_login_password("", "")
        self.login_page.find(self.login_page.locators.LOGIN_BUTTON)

    @pytest.mark.usefixtures("take_screenshot_when_failure")
    @pytest.mark.UI
    def test_vk_id_positive(self, stable_user):
        """Тест проверяет наличие vk_id на главнй странице.

        Стабильный пользователь авторизуется, проверяется наличие формы с vk_id и ее содержимое.
        """
        user, _ = stable_user
        self.login_page.send_login_password(user["username"], user["password"])
        element = self.main_page.find(self.main_page.locators.VK_ID_FRAME)
        assert user["vk_id"] in element.text.lower()

    @pytest.mark.usefixtures("take_screenshot_when_failure")
    @pytest.mark.UI
    def test_vk_id_negative(self, random_user):
        """Тест проверяет отсутсвие vk_id у рандомного пользователя.

        Рандомный пользователь регистрируется, авторизуется.
        Проверяется отсутсвие содержимого у формы с vk_id.
        """
        self.login_page.click(self.login_page.locators.REG_BUTTON)
        self.registration_page.registration(random_user)
        element = self.main_page.find(self.main_page.locators.VK_ID_FRAME)
        assert "" in element.text.lower()

    @pytest.mark.usefixtures("take_screenshot_when_failure")
    @pytest.mark.UI
    def test_logout(self, stable_user):
        """Тест проверяет завершение сессии при нажатии на кнопку logout.

        Стабильный пользователь авторизуется, происходит нажатие на кнопку logout,
        проверяется переход на страницу авторизации.
        """
        user, _ = stable_user
        self.login_page.send_login_password(user["username"], user["password"])
        self.main_page.click(self.main_page.locators.LOGOUT_BUTTON)
        self.login_page.find(self.login_page.locators.LOGIN_BUTTON)

    @pytest.mark.usefixtures("take_screenshot_when_failure")
    @pytest.mark.UI
    def test_registration_positive(self, random_user):
        """Тест проверяет успешную регистрацию.

        Случайный пользователь производит корректное заполнение всех форм,
        проверяется наличие формы с именем пользователя и ее содержимое на главной странице.
        """
        self.login_page.click(self.login_page.locators.REG_BUTTON)
        self.registration_page.registration(random_user)
        element = self.main_page.find(self.main_page.locators.LOGIN_FRAME)
        assert random_user["username"] in element.text.lower()

    @pytest.mark.usefixtures("take_screenshot_when_failure")
    @pytest.mark.UI
    def test_registration_positive_symbols(self, random_user):
        """Тест проверяет успешную регистрацию.

        Случайный пользователь производит корректное заполнение всех форм, поле username
        заполняется специальными символами,
        проверяется наличие формы с именем пользователя и ее содержимое на главной странице.
        """
        random_user["username"] = "a!#$%&*~"
        self.login_page.click(self.login_page.locators.REG_BUTTON)
        self.registration_page.registration(random_user)
        element = self.main_page.find(self.main_page.locators.LOGIN_FRAME)
        assert random_user["username"] in element.text.lower()

    @pytest.mark.parametrize("users", [["123123", "1235@yandex.ru", "123", "321", ['Passwords must match'.lower(), ]],
                                       ["123", "1234@yandex.ru", "123", "123", ['Incorrect username length'.lower(), ]],
                                       ["123987", "1234yandex.ru", "123", "123", ['invalid email address'.lower(), ]],
                                       ["1", "1", "1", "2", ['Passwords must match'.lower(),
                                                             'Incorrect username length'.lower(),
                                                             'Incorrect email length'.lower()]],
                                       ["789123", "789@yandex.ru", "1"*256, "1"*256,
                                        ['Incorrect password length'.lower(), ]],
                                       ["5"*17, "555@yandex.ru", "123", "123", ['Incorrect username length'.lower(), ]]
                                       ])
    @pytest.mark.usefixtures("take_screenshot_when_failure")
    @pytest.mark.UI
    def test_registration_negative(self, users):
        """Тест проверяет негативную регистрацию.

        Проверяются случаи:
        1) несовпадение пароля
        2), 6) некорректная длина имени пользователя
        3) некорректность почтового адреса
        4) несовпадение пароля и некорректная длина имени пользователя и некорректная длина почтового адреса
        5) некорректная длина пароля
        Проверяется текст всплывающего уведомления.
        """
        self.login_page.click(self.login_page.locators.REG_BUTTON)
        self.registration_page.registration({"username": users[0],
                                             "email": users[1],
                                             "password": users[2],
                                             "confirm": users[3]
                                             })
        element = self.registration_page.find(self.registration_page.locators.FLASH_FRAME)
        element_text = element.get_attribute("textContent").lower()
        for condition in users[4]:
            assert condition in element_text

    @pytest.mark.usefixtures("take_screenshot_when_failure")
    @pytest.mark.UI
    def test_go_home(self, stable_user):
        """Тест проверяет переход на домашнюю страницу при нажатии на кнопку Home.

        Стабильный пользователь авторизуется, происходит нажатие на элемент Home,
        проверяется наличие формы с именем пользователя и ее содержимое на главной странице.
        """
        user, _ = stable_user
        self.login_page.send_login_password(user["username"], user["password"])
        self.main_page.go_to_home()
        element = self.main_page.find(self.main_page.locators.LOGIN_FRAME)
        assert user["username"] in element.text.lower()

    @pytest.mark.usefixtures("take_screenshot_when_failure")
    @pytest.mark.UI
    def test_go_python(self, stable_user):
        """Тест проверяет переход на страницу Pytrhon.org при нажатии на кнопку Python.

        Стабильный пользователь авторизуется, происходит нажатие на элемент Python,
        проверяется наличие элемента с изображением на главной странице Python.org.
        """
        user, _ = stable_user
        self.login_page.send_login_password(user["username"], user["password"])
        self.main_page.go_to_python()
        self.python_page.find(self.python_page.locators.PYTHON_IMG)

    @pytest.mark.usefixtures("take_screenshot_when_failure")
    @pytest.mark.UI
    def test_go_wikipedia_history(self, stable_user):
        """Тест проверяет переход на страницу https://en.wikipedia.org/wiki/History_of_Python
         при нажатии на элемент выпадающего списка.

        Стабильный пользователь авторизуется, происходит наведение на элемент Python,
        нажимается элемент выпадающего списка Python history,
        проверяется наличие элемента с надписью History of Python на странице en.wikipedia.org.
        """
        user, _ = stable_user
        self.login_page.send_login_password(user["username"], user["password"])
        ac = ActionChains(self.driver)
        self.main_page.go_to_wikipedia_history(ac)
        element = self.wikipedia_page.find(self.wikipedia_page.locators.WIKIPEDIA_TITLE)
        assert "history of python" in element.text.lower()

    @pytest.mark.usefixtures("take_screenshot_when_failure")
    @pytest.mark.UI
    def test_go_flask(self, stable_user):
        """Тест проверяет переход на страницу https://flask.palletsprojects.com/en/1.1.x/#
         при нажатии на элемент выпадающего списка.

        Стабильный пользователь авторизуется, происходит наведение на элемент Python,
        нажимается элемент выпадающего списка About Flask,
        проверяется наличие элемента с изображением на странице flask.palletsprojects.com.
        """
        user, _ = stable_user
        self.login_page.send_login_password(user["username"], user["password"])
        ac = ActionChains(self.driver)
        before_page = self.main_page.go_to_flask(ac)
        self.flask_page.find(self.flask_page.locators.FLASK_IMG)
        self.main_page.go_back(before_page)

    @pytest.mark.usefixtures("take_screenshot_when_failure")
    @pytest.mark.UI
    def test_go_download_centos(self, stable_user):
        """Тест проверяет переход на страницу https://getfedora.org/ru/workstation/download/
         при нажатии на элемент выпадающего списка.

        Стабильный пользователь авторизуется, происходит наведение на элемент linux,
        нажимается элемент выпадающего списка Download Centos7,
        проверяется наличие элемента с изображением на странице getfedora.org/ru/workstation/download/
        """
        user, _ = stable_user
        self.login_page.send_login_password(user["username"], user["password"])
        ac = ActionChains(self.driver)
        before_page = self.main_page.go_to_centos(ac)
        self.linux_page.find(self.linux_page.locators.FEDORA_IMG)
        self.main_page.go_back(before_page)

    @pytest.mark.usefixtures("take_screenshot_when_failure")
    @pytest.mark.UI
    def test_go_to_wireshark_download(self, stable_user):
        """Тест проверяет переход на страницу https://www.wireshark.org/#download
        при нажатии на элемент выпадающего списка.

        Стабильный пользователь авторизуется, происходит наведение на элемент Network,
        нажимается элемент выпадающего списка WIRESHARK: DOWNLOAD,
        проверяется наличие элемента загрузки на странице www.wireshark.org/#download
        """
        user, _ = stable_user
        self.login_page.send_login_password(user["username"], user["password"])
        ac = ActionChains(self.driver)
        before_page = self.main_page.go_to_wireshark_download(ac)
        self.wireshark_page.find(self.wireshark_page.locators.DOWNLOAD_HEADER)
        self.main_page.go_back(before_page)

    @pytest.mark.usefixtures("take_screenshot_when_failure")
    @pytest.mark.UI
    def test_go_to_wireshark_news(self, stable_user):
        """Тест проверяет переход на страницу https://www.wireshark.org/news/
        при нажатии на элемент выпадающего списка.

        Стабильный пользователь авторизуется, происходит наведение на элемент Network,
        нажимается элемент выпадающего списка WIRESHARK: NEWS,
        проверяется наличие элемента Go Beyond with Riverbed Technology на странице www.wireshark.org/news/
        """
        user, _ = stable_user
        self.login_page.send_login_password(user["username"], user["password"])
        ac = ActionChains(self.driver)
        before_page = self.main_page.go_to_wireshark_news(ac)
        self.wireshark_page.find(self.wireshark_page.locators.GO_BEYOND_DIV)
        self.main_page.go_back(before_page)

    @pytest.mark.usefixtures("take_screenshot_when_failure")
    @pytest.mark.UI
    def test_go_to_tcp_dump_examples(self, stable_user):
        """Тест проверяет переход на страницу https://hackertarget.com/tcpdump-examples/
        при нажатии на элемент выпадающего списка.

        Стабильный пользователь авторизуется, происходит наведение на элемент Network,
        нажимается элемент выпадающего списка TCPDUMP: EXAMPLES,
        проверяется наличие элемента Tcpdump Examples на странице hackertarget.com/tcpdump-examples/
        """
        user, _ = stable_user
        self.login_page.send_login_password(user["username"], user["password"])
        ac = ActionChains(self.driver)
        before_page = self.main_page.go_to_tcp_dump_examples(ac)
        self.tcp_dump_page.find(self.tcp_dump_page.locators.TCP_DUMP_EXAMPLE_H1)
        self.main_page.go_back(before_page)

    @pytest.mark.usefixtures("take_screenshot_when_failure")
    @pytest.mark.UI
    def test_go_to_wikipedia_api(self, stable_user):
        """Тест проверяет переход на страницу https://en.wikipedia.org/wiki/Application_programming_interface
        при нажатии на центральный элемент What is an API?.

        Стабильный пользователь авторизуется, происходит наведение и нажатие на элемент What is an API?,
        проверяется наличие элемента с надписью Application programming interface на странице
        en.wikipedia.org/wiki/Application_programming_interface
        """
        user, _ = stable_user
        self.login_page.send_login_password(user["username"], user["password"])
        ac = ActionChains(self.driver)
        before_page = self.main_page.go_to_wikipedia_api(ac)
        element = self.wikipedia_page.find(self.wikipedia_page.locators.WIKIPEDIA_TITLE)
        assert "application programming interface" in element.text.lower()
        self.main_page.go_back(before_page)

    @pytest.mark.usefixtures("take_screenshot_when_failure")
    @pytest.mark.UI
    def test_go_to_popular_mechanic(self, stable_user):
        """Тест проверяет переход на страницу
        https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/
        при нажатии на центральный элемент Future of internet.

        Стабильный пользователь авторизуется, происходит наведение и нажатие на элемент Future of internet,
        проверяется наличие элемента с надписью What Will the Internet Be Like in the Next 50 Years? на странице
        www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/
        """
        user, _ = stable_user
        self.login_page.send_login_password(user["username"], user["password"])
        ac = ActionChains(self.driver)
        before_page = self.main_page.go_to_popular_mechanic(ac)
        element = self.popular_mechanic_page.find(self.popular_mechanic_page.locators.INTERNET_HEADER_H1)
        assert "What Will the Internet Be Like in the Next 50 Years?".lower() in element.text.lower()
        self.main_page.go_back(before_page)

    @pytest.mark.usefixtures("take_screenshot_when_failure")
    @pytest.mark.UI
    def test_go_to_wikipedia_smtp(self, stable_user):
        """Тест проверяет переход на страницу https://ru.wikipedia.org/wiki/SMTP
        при нажатии на центральный элемент Lets talk about SMTP?.

        Стабильный пользователь авторизуется, происходит наведение и нажатие на элемент Lets talk about SMTP?,
        проверяется наличие элемента с надписью SMTP на странице
        ru.wikipedia.org/wiki/SMTP
        """
        user, _ = stable_user
        self.login_page.send_login_password(user["username"], user["password"])
        ac = ActionChains(self.driver)
        before_page = self.main_page.go_to_wikipedia_smtp(ac)
        element = self.wikipedia_page.find(self.wikipedia_page.locators.WIKIPEDIA_TITLE)
        assert "SMTP".lower() in element.text.lower()
        self.main_page.go_back(before_page)

    @pytest.mark.usefixtures("take_screenshot_when_failure")
    @pytest.mark.UI
    def test_python_facts(self, stable_user):
        """Тест проверяет наличие элемента со случайными надписями о языке Python
        на главной странице.

        Стабильный пользователь авторизуется, производится поиск элемента со случайными фактами
        на странице, проверяется равенство с пустой строкой
        ru.wikipedia.org/wiki/SMTP
        """
        user, _ = stable_user
        self.login_page.send_login_password(user["username"], user["password"])
        element = self.main_page.find(self.main_page.locators.PYTHON_FACT_P)
        assert "" != element.text

    @pytest.mark.usefixtures("take_screenshot_when_failure")
    @pytest.mark.UI
    def test_tm_version_button(self, stable_user):
        """Тест проверяет переход на домашнюю страницу при нажатии на кнопку TM Version 0.1.

        Стабильный пользователь авторизуется, происходит нажатие на элемент TM Version 0.1,
        проверяется наличие формы с именем пользователя и ее содержимое на главной странице.
        """
        user, _ = stable_user
        self.login_page.send_login_password(user["username"], user["password"])
        self.main_page.click(self.main_page.locators.TM_VERSION_BUTTON)
        element = self.main_page.find(self.main_page.locators.LOGIN_FRAME)
        assert user["username"] in element.text.lower()
