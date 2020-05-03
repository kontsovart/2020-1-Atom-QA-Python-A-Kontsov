from random import randint

import pytest

from models.models import LogFile, Task1, Task2, Task3, Task4, Task5
from mysql_orm_client.mysql_orm_client import MysqlOrmConnection
from builder.orm_builder import MysqlOrmBuilder


class TestOrmMysql:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_orm_client):
        self.mysql: MysqlOrmConnection = mysql_orm_client
        self.builder = MysqlOrmBuilder(mysql_orm_client)

    def test_task1_delete(self):
        logfile = self.builder.add_logfile(name='file1')

        for i in range(10):
            self.builder.add_task1(count=i, file_id=logfile.id)

        res = self.mysql.session.query(Task1).filter_by(id=10).one()
        assert res.counter == 9
