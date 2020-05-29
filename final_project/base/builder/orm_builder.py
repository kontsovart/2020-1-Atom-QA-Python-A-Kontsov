from base.models.models import Base, UsersTest
from base.mysql_orm_client.mysql_orm_client import MysqlOrmConnection


class MysqlOrmBuilder:

    def __init__(self, connection: MysqlOrmConnection):
        self.connection = connection
        self.engine = connection.connection.engine

    def create_test_users(self):
        if not self.engine.dialect.has_table(self.engine, 'test_users'):
            Base.metadata.tables['test_users'].create(self.engine)
        else:
            Base.metadata.tables['test_users'].drop(self.engine)
            Base.metadata.tables['test_users'].create(self.engine)

    def add_user(self, username, password, email, access, active, start_active_time):
        user = UsersTest(
            username=username,
            password=password,
            email=email,
            access=access,
            active=active,
            start_active_time=start_active_time
        )
        self.connection.session.add(user)
        self.connection.session.commit()

        return user
