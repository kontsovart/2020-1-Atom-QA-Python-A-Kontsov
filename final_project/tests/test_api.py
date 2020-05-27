import pytest

from api.myapp_client import MailAppClient
from ui.fixtures import *
from base.models.models import UsersTest
from datetime import datetime


class TestMailAppClient:

    @pytest.fixture(scope='function')
    def api_client_stable(self, stable_user, config):
        user, _ = stable_user
        client = MailAppClient(user=user["username"],
                               password=user["password"],
                               email=user["email"],
                               url=config["url_app"])
        return client

    @pytest.fixture(scope='function')
    def api_client_function(self, random_user, config):
        return MailAppClient(user=random_user["username"],
                             password=random_user["password"],
                             email=random_user["email"],
                             url=config["url_app"])

    @pytest.mark.API
    def test_auth_positive(self, api_client_stable, setup_base):
        """Тест проверяет успешную авторизацию.

        Стабильный пользователь авторизуется, проверяется код ответа и значение поля active в таблице.
        """
        mysql, _ = setup_base
        response = api_client_stable.auth_post()
        mysql.session.commit()
        res = mysql.session.query(UsersTest).filter_by(username=api_client_stable.user).first()
        assert 200 == response.status_code
        assert res.active == 1

    # Test failed on user_pass1
    @pytest.mark.parametrize("user_pass", [["123123", "123"],
                                           ["123", "123"],
                                           ["", "123"],
                                           ["123123", ""],
                                           ["", ""],
                                           ["1" * 17, "123"],
                                           ["1231231", "1" * 256]])
    @pytest.mark.API
    def test_auth_negative(self, user_pass, config):
        """Тест проверяет негативную авторизацию.

        Проверяются случаи:
        1) остуствие пользователя в базе данных
        2), 3), 6) некорректная длина имени пользователя
        4), 7) некорректная длина пароля
        5) некорректная длина имени пользователя и некорректная длина пароля
        Проверяется код ответа.
        """
        client = MailAppClient(user=user_pass[0],
                               password=user_pass[1],
                               email=None,
                               url=config["url_app"])
        response = client.auth_post()
        assert 401 == response.status_code

    @pytest.mark.API
    def test_get_welcome_page(self, api_client_stable):
        """Тест проверяет получение домашней страницы.

        Стабильный пользователь авторизуется, запрашивается домашняя страница
        проверяется код ответа.
        """
        api_client_stable.auth_post()
        response = api_client_stable.get_welcome_page()
        assert 200 == response.status_code

    @pytest.mark.API
    def test_get_login_page(self, api_client_stable):
        """Тест проверяет получение страницы авторизации.

        Запрашивается страницы авторизации,
        проверяется код ответа.
        """
        response = api_client_stable.get_login_page()
        assert 200 == response.status_code

    @pytest.mark.API
    def test_get_registration_page(self, api_client_function):
        """Тест проверяет получение страницы регистрации.

        Запрашивается страницы регистрации,
        проверяется код ответа.
        """
        response = api_client_function.get_registration_page()
        assert 200 == response.status_code

    # Test failed
    @pytest.mark.API
    def test_get_find_me_error(self, api_client_stable):
        """Тест проверяет получение элемента при загрузке домашней страницы.

        Запрашивается элемент,
        проверяется код ответа.
        """
        api_client_stable.auth_post()
        response = api_client_stable.get_find_me_error()
        assert 200 == response.status_code

    @pytest.mark.API
    def test_logout_get(self, api_client_function, setup_base):
        """Тест проверяет завершение сессии при нажатии на кнопку logout.

        Случайный пользователь добавляется в базу данных, авторизуется, запрашивается logout,
        проверяется код ответа и значение поля active в таблице .
        """
        mysql, builder = setup_base

        builder.add_user(username=api_client_function.user,
                         password=api_client_function.password,
                         email=api_client_function.email,
                         access=1,
                         active=0,
                         start_active_time=datetime.now())
        api_client_function.auth_post()
        response = api_client_function.logout_get()
        res = mysql.session.query(UsersTest).filter_by(username=api_client_function.user).first()
        assert 200 == response.status_code
        assert res.active == 0

    @pytest.mark.API
    def test_registration_post_positive(self, api_client_function, setup_base):
        """Тест проверяет успешную регистрацию.

        Случайный пользователь производит корректное заполнение всех форм,
        проверяется код ответа и наличие записи в базе данных.
        """
        mysql, _ = setup_base
        response = api_client_function.registration_post()
        mysql.session.commit()
        res = mysql.session.query(UsersTest).filter_by(username=api_client_function.user).first()
        assert 200 == response.status_code
        assert res is not None

    # Test failed
    @pytest.mark.API
    def test_registration_post_negative_user(self, api_client_stable, random_string_ascii, setup_base, config):
        """Тест проверяет негативную регистрацию.

       Проверяется случай совпадения имени пользователя с уже существующим.
       Случайный пользователь производит регистрацию, используя имя стабильного пользователя,
       проверяется код ответа и количество записей в базе данных
       """
        mysql, _ = setup_base
        api_client_stable.registration_post()
        client = MailAppClient(user=api_client_stable.user,
                               password=api_client_stable.password,
                               email=random_string_ascii+'@yandex.ru',
                               url=config["url_app"])
        response = client.registration_post()
        mysql.session.commit()
        res = mysql.session.query(UsersTest).filter_by(username=api_client_stable.user).all()
        assert 400 == response.status_code
        assert len(res) == 1

    # Test failed
    @pytest.mark.API
    def test_registration_post_negative_email(self, api_client_stable, random_string_ascii, setup_base, config):
        """Тест проверяет негативную регистрацию.

       Проверяется случай совпадения email пользователя с уже существующим.
       Случайный пользователь производит регистрацию, используя email стабильного пользователя,
       проверяется код ответа и количество записей в базе данных
       """
        mysql, _ = setup_base
        api_client_stable.registration_post()
        client = MailAppClient(user=random_string_ascii,
                               password=api_client_stable.password,
                               email=api_client_stable.email,
                               url=config["url_app"])
        response = client.registration_post()
        mysql.session.commit()
        res = mysql.session.query(UsersTest).filter_by(username=api_client_stable.user).all()
        assert 400 == response.status_code
        assert len(res) == 1

    # Test failed on user9, user11
    @pytest.mark.parametrize("users", [[None, None, "123", "321"],
                                       ["123", None, "123", "123"],
                                       [None, "@yandex.ru", "123", "123"],
                                       [None, "123@yandex", "123", "123"],
                                       [None, "123@.ru", "123", "123"],
                                       [None, "@.ru", "123", "123"],
                                       [None, "@.", "123", "123"],
                                       [None, "@", "123", "123"],
                                       [None, ".", "123", "123"],
                                       [None, "123@yandex.r", "123", "123"],
                                       [None, "12", "123", "123"],
                                       [None, None, "1" * 256, "1" * 256],
                                       ["1" * 17, None, "123", "123"],
                                       ["1", "1", "1", "2"]])
    @pytest.mark.API
    def test_registration_post_negative_all(self, users, setup_base, random_string_ascii, config):
        """Тест проверяет негативную регистрацию.

       Проверяются случаи:
       1) несовпадение пароля
       2), 13) некорректная длина имени пользователя
       3)-11) некорректный формат email
       12) некорректная длина пароля
       14) несовпадение пароля и некорректная длина имени пользователя и некорректность почтового адреса
       Случайный пользователь производит регистрацию, используя невалидные формы,
       проверяется код ответа и отсутсвие записи в базе данных.
       """
        mysql, _ = setup_base
        client = MailAppClient(user=users[0] if users[0] else random_string_ascii,
                               password=users[2],
                               email=users[1] if users[1] else random_string_ascii + "@yandex.ru",
                               url=config["url_app"])
        response = client.registration_post(confirm=users[3])
        mysql.session.commit()
        res = mysql.session.query(UsersTest).filter_by(username=users[0]).first()
        assert 400 == response.status_code
        assert res is None

    @pytest.mark.API
    def test_registration_post_empty(self, api_client_function):
        """Тест проверяет негативную регистрацию пользователя.

        Отправляется POST запрос на регистрацию пользователя,
        в котором отсутсвуют правильные данные, проверяется код ответа
        """
        response = api_client_function.registration_post(empty=True)
        assert 400 == response.status_code

    # Test failed
    @pytest.mark.API
    def test_add_user_post(self, api_client_stable, random_user, setup_base):
        """Тест проверяет успешное добавление пользователя.

        Стабильный пользователь авторизуется, происходит добавление новго случайного пользователя,
        проверяется код ответа и наличие записи в базе данных
        """
        mysql, builder = setup_base
        api_client_stable.auth_post()
        response = api_client_stable.add_user_post(user=random_user["username"],
                                                   password=random_user["password"],
                                                   email=random_user["email"])
        mysql.session.commit()
        res = mysql.session.query(UsersTest).filter_by(username=random_user["username"]).first()
        assert 201 == response.status_code
        assert res is not None

    @pytest.mark.API
    def test_add_user_post_negative_username(self, api_client_stable, random_user, setup_base):
        """Тест проверяет негативное добавление пользователя.

        Стабильный пользователь авторизуется, происходит добавление новго случайного пользователя c
        уже существующим username,
        проверяется код ответа и наличие записи в базе данных
        """
        mysql, builder = setup_base
        api_client_stable.auth_post()
        response = api_client_stable.add_user_post(user=api_client_stable.user,
                                                   password=random_user["password"],
                                                   email=random_user["email"])
        mysql.session.commit()
        res = mysql.session.query(UsersTest).filter_by(username=api_client_stable.user).all()
        assert 400 == response.status_code
        assert len(res) == 1

    @pytest.mark.API
    def test_add_user_post_negative_email(self, api_client_stable, random_user, setup_base):
        """Тест проверяет негативное добавление пользователя.

        Стабильный пользователь авторизуется, происходит добавление новго случайного пользователя c
        уже существующим email,
        проверяется код ответа и наличие записи в базе данных
        """
        mysql, builder = setup_base
        api_client_stable.auth_post()
        response = api_client_stable.add_user_post(user=random_user["username"],
                                                   password=random_user["password"],
                                                   email=api_client_stable.email)
        mysql.session.commit()
        res = mysql.session.query(UsersTest).filter_by(email=api_client_stable.email).all()
        assert 400 == response.status_code
        assert len(res) == 1

    @pytest.mark.API
    def test_add_user_post_empty(self, api_client_stable):
        """Тест проверяет негативное добавление пользователя.

        Стабильный пользователь авторизуется, отправляется POST запрос на добавление пользователя,
        в котом отсутсвуют правильные заголовки и данные,
        проверяется код ответа
        """
        api_client_stable.auth_post()
        response = api_client_stable.add_user_post(empty=True)
        assert 400 == response.status_code

    @pytest.mark.API
    def test_add_user_get(self, api_client_stable):
        """Тест проверяет негативное добавление пользователя.

        Стабильный пользователь авторизуется, отправляется GET запрос на добавление пользователя,
        в котом отсутсвуют правильные заголовки и данные,
        проверяется код ответа
        """
        api_client_stable.auth_post()
        response = api_client_stable.add_user_get()
        assert 404 == response.status_code

    @pytest.mark.API
    def test_del_user_positive(self, api_client_function, setup_base):
        """Тест проверяет успешное удаление пользователя.

        Случайный пользователь, авторизуется, отправляется GET запрос на удаление пользователя,
        проверяется код ответа и отсутствие записи в базе данных.
        """
        mysql, _ = setup_base
        api_client_function.registration_post()
        response = api_client_function.del_user_get()
        mysql.session.commit()
        res = mysql.session.query(UsersTest).filter_by(username=api_client_function.user).first()
        assert 204 == response.status_code
        assert res is None

    @pytest.mark.API
    def test_del_user_negative_not_auth(self, api_client_function, setup_base):
        """Тест проверяет негативное удаление пользователя.

        Случайный пользователь добавляется в базу данных, отправляется GET запрос на удаление пользователя,
        проверяется код ответа и наличие записи в базе данных.
        """
        mysql, builder = setup_base

        builder.add_user(username=api_client_function.user,
                         password=api_client_function.password,
                         email=api_client_function.email,
                         access=1,
                         active=0,
                         start_active_time=datetime.now())
        response = api_client_function.del_user_get(user=api_client_function.user)
        mysql.session.commit()
        res = mysql.session.query(UsersTest).filter_by(username=api_client_function.user).first()
        assert 401 == response.status_code
        assert res is not None

    @pytest.mark.API
    def test_del_user_negative_not_exists(self, api_client_stable, random_string_ascii, setup_base):
        """Тест проверяет негативное удаление пользователя.

        Cтабильный пользователь авторизуется, отправляется GET запрос на удаление не существующего пользователя,
        проверяется код ответа и отсутствие записи в базе данных.
        """
        mysql, _ = setup_base
        api_client_stable.auth_post()
        response = api_client_stable.del_user_get(random_string_ascii)
        mysql.session.commit()
        res = mysql.session.query(UsersTest).filter_by(username=random_string_ascii).first()
        assert 404 == response.status_code
        assert res is None

    @pytest.mark.API
    def test_del_user_empty(self, api_client_stable):
        """Тест проверяет негативное удаление пользователя.

        Cтабильный пользователь авторизуется, отправляется GET запрос на удаление без username,
        проверяется код ответа.
        """
        api_client_stable.auth_post()
        response = api_client_stable.del_user_get(empty=True)
        assert 404 == response.status_code

    @pytest.mark.API
    def test_block_user_positive(self, api_client_function, setup_base):
        """Тест проверяет успешную блокировку пользователя.

        Случайный пользователь регистрируется, отправляется GET запрос на блокировку пользователя,
        проверяется код ответа и значение поля access в таблице.
        """
        mysql, _ = setup_base
        api_client_function.registration_post()
        response = api_client_function.block_user_get()
        mysql.session.commit()
        res = mysql.session.query(UsersTest).filter_by(username=api_client_function.user).first()
        assert 200 == response.status_code
        assert res.access == 0

    @pytest.mark.API
    def test_block_user_negative_not_auth(self, api_client_function, setup_base):
        """Тест проверяет негативную блокировку пользователя.

        Случайный пользователь добавляетя в базу данных, отправляется GET запрос на блокировку пользователя
        без авторизации, проверяется код ответа и значение поля access в таблице.
        """
        mysql, builder = setup_base

        builder.add_user(username=api_client_function.user,
                         password=api_client_function.password,
                         email=api_client_function.email,
                         access=1,
                         active=0,
                         start_active_time=datetime.now())
        response = api_client_function.block_user_get(user=api_client_function.user)
        mysql.session.commit()
        res = mysql.session.query(UsersTest).filter_by(username=api_client_function.user).first()
        assert 401 == response.status_code
        assert res.access == 1

    @pytest.mark.API
    def test_block_user_negative_not_exists(self, api_client_stable, random_string_ascii, setup_base):
        """Тест проверяет негативную блокировку пользователя.

        Стабильный пользователь авторизуется, отправляется GET запрос на блокировку случайного пользователя,
        проверяется код ответа и отсутствие записи в таблице.
        """
        mysql, _ = setup_base
        api_client_stable.auth_post()
        response = api_client_stable.block_user_get(random_string_ascii)
        mysql.session.commit()
        res = mysql.session.query(UsersTest).filter_by(username=random_string_ascii).first()
        assert 404 == response.status_code
        assert res is None

    @pytest.mark.API
    def test_block_user_empty(self, api_client_stable):
        """Тест проверяет негативную блокировку пользователя.

        Стабильный пользователь авторизуется, отправляется GET запрос на блокировку пользователя без username,
        проверяется код ответа.
        """
        response = api_client_stable.block_user_get(empty=True)
        assert 404 == response.status_code

    @pytest.mark.API
    def test_accept_user_positive(self, api_client_function, api_client_stable, setup_base):
        """Тест проверяет успешную разблокировку пользователя.

        Случайный пользователь добавляется в базу данных с access=0, стабильный пользователь авторизуется,
        отправляется GET запрос на разблокировку пользователя,
        проверяется код ответа и поле access в базе данных.
        """
        mysql, builder = setup_base

        builder.add_user(username=api_client_function.user,
                         password=api_client_function.password,
                         email=api_client_function.email,
                         access=0,
                         active=0,
                         start_active_time=datetime.now())
        api_client_stable.auth_post()
        response = api_client_stable.accept_user_get(user=api_client_function.user)
        mysql.session.commit()
        res = mysql.session.query(UsersTest).filter_by(username=api_client_function.user).first()
        assert 200 == response.status_code
        assert res.access == 1

    @pytest.mark.API
    def test_accept_user_negative_not_auth(self, api_client_function, api_client_stable, setup_base):
        """Тест проверяет негативную разблокировку пользователя.

       Случайный пользователь добавляется в базу данных с access=0,
       отправляется GET запрос на разблокировку пользователя без авторизации,
       проверяется код ответа и поле access в базе данных.
       """
        mysql, builder = setup_base

        builder.add_user(username=api_client_function.user,
                         password=api_client_function.password,
                         email=api_client_function.email,
                         access=0,
                         active=0,
                         start_active_time=datetime.now())
        response = api_client_stable.accept_user_get(user=api_client_function.user)
        mysql.session.commit()
        res = mysql.session.query(UsersTest).filter_by(username=api_client_function.user).first()
        assert 401 == response.status_code
        assert res.access == 0

    @pytest.mark.API
    def test_accept_user_negative_not_exists(self, api_client_stable, random_string_ascii, setup_base):
        """Тест проверяет негативную разблокировку пользователя.

        Стабильный пользователь авторизуется,
        отправляется GET запрос на разблокировку не существующего пользователя,
        проверяется код ответа и отсутствие записи в базе данных.
        """
        mysql, _ = setup_base
        api_client_stable.auth_post()
        response = api_client_stable.accept_user_get(random_string_ascii)
        mysql.session.commit()
        res = mysql.session.query(UsersTest).filter_by(username=random_string_ascii).first()
        assert 404 == response.status_code
        assert res is None

    @pytest.mark.API
    def test_accept_user_empty(self, api_client_stable):
        """Тест проверяет негативную разблокировку пользователя.

        Стабильный пользователь авторизуется,
        отправляется GET запрос на разблокировку без указания username,
        проверяется код ответа.
        """
        api_client_stable.auth_post()
        response = api_client_stable.accept_user_get(empty=True)
        assert 404 == response.status_code

    @pytest.mark.API
    def test_get_app_status(self, api_client_stable):
        """Тест проверяет успешное получение статуса приложения.

        Стабильный пользователь авторизуется,
        отправляется GET запрос на получение статуса приложения,
        проверяется код ответа и полученные данные.
        """
        api_client_stable.auth_post()
        response = api_client_stable.status_app_get()
        assert 200 == response.status_code
        assert '{"status":"ok"}' == response.text.strip()

    @pytest.mark.API
    def test_get_app_status_not_auth(self, api_client_stable):
        """Тест проверяет успешное получение статуса приложения.

        Отправляется GET запрос на получение статуса приложения,
        проверяется код ответа и полученные данные.
        """
        response = api_client_stable.status_app_get()
        assert 200 == response.status_code
        assert '{"status":"ok"}' == response.text.strip()
