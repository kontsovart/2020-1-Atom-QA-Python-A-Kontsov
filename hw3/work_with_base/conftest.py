import pytest
from mysql_orm_client.mysql_orm_client import MysqlOrmConnection


@pytest.fixture(scope='session')
def mysql_orm_client():
    return MysqlOrmConnection('root', 'pass', 'HW3_work_base', '127.0.0.1', 3306)
