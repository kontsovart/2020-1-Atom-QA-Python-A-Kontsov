from models import Base, LogFile, Task1, Task2, Task3, Task4, Task5
from mysql_orm_client import MysqlOrmConnection


class MysqlOrmBuilder:

    def __init__(self, connection: MysqlOrmConnection):
        self.connection = connection
        self.engine = connection.connection.engine
        self.create_files()
        self.create_task1()
        self.create_task2()
        self.create_task3()
        self.create_task4()
        self.create_task5()

    def create_files(self):
        if not self.engine.dialect.has_table(self.engine, 'logfiles'):
            Base.metadata.tables['logfiles'].create(self.engine)

    def create_task1(self):
        if not self.engine.dialect.has_table(self.engine, 'task1'):
            Base.metadata.tables['task1'].create(self.engine)

    def create_task2(self):
        if not self.engine.dialect.has_table(self.engine, 'task2'):
            Base.metadata.tables['task2'].create(self.engine)

    def create_task3(self):
        if not self.engine.dialect.has_table(self.engine, 'task3'):
            Base.metadata.tables['task3'].create(self.engine)

    def create_task4(self):
        if not self.engine.dialect.has_table(self.engine, 'task4'):
            Base.metadata.tables['task4'].create(self.engine)

    def create_task5(self):
        if not self.engine.dialect.has_table(self.engine, 'task5'):
            Base.metadata.tables['task5'].create(self.engine)
