from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class LogFile(Base):
    __tablename__ = 'logfiles'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<Prepod(" \
               f"id='{self.id}'," \
               f"name='{self.name}')>"


class Task1(Base):
    __tablename__ = 'task1'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    counter = Column(Integer, nullable=False)
    file_id = Column(Integer, ForeignKey(f'{LogFile.__tablename__}.{LogFile.id.name}'), nullable=False)

    def __repr__(self):
        return f"<Student(" \
               f"id='{self.id}'," \
               f"counter='{self.counter}', " \
               f"file_id='{self.file_id}'" \
               f")>"


class Task2(Base):
    __tablename__ = 'task2'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    request_type = Column(String(10), nullable=False)
    counter = Column(Integer, nullable=False)
    file_id = Column(Integer, ForeignKey(f'{LogFile.__tablename__}.{LogFile.id.name}'), nullable=False)

    def __repr__(self):
        return f"<Student(" \
               f"id='{self.id}'," \
               f"request_type='{self.request_type}', " \
               f"counter='{self.counter}', " \
               f"file_id='{self.file_id}'" \
               f")>"


class Task3(Base):
    __tablename__ = 'task3'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    request_type = Column(String(10), nullable=False)
    url = Column(String(100), nullable=False)
    ip = Column(String(40), nullable=False)
    date = Column(String(50), nullable=False)
    size = Column(Integer, nullable=False)
    file_id = Column(Integer, ForeignKey(f'{LogFile.__tablename__}.{LogFile.id.name}'), nullable=False)

    def __repr__(self):
        return f"<Student(" \
               f"id='{self.id}'," \
               f"request_type='{self.request_type}', " \
               f"url='{self.url}', "\
               f"ip='{self.ip}', " \
               f"date='{self.date}', " \
               f"size='{self.size}', " \
               f"file_id='{self.file_id}'" \
               f")>"


class Task4(Base):
    __tablename__ = 'task4'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    request_type = Column(String(10), nullable=False)
    url = Column(String(100), nullable=False)
    error_code = Column(Integer, nullable=False)
    ip = Column(String(40), nullable=False)
    file_id = Column(Integer, ForeignKey(f'{LogFile.__tablename__}.{LogFile.id.name}'), nullable=False)

    def __repr__(self):
        return f"<Student(" \
               f"id='{self.id}'," \
               f"request_type='{self.request_type}', " \
               f"url='{self.url}', "\
               f"error_code='{self.error_code}', " \
               f"ip='{self.ip}', " \
               f"file_id='{self.file_id}'" \
               f")>"


class Task5(Base):
    __tablename__ = 'task5'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    request_type = Column(String(10), nullable=False)
    url = Column(String(100), nullable=False)
    error_code = Column(Integer, nullable=False)
    ip = Column(String(40), nullable=False)
    file_id = Column(Integer, ForeignKey(f'{LogFile.__tablename__}.{LogFile.id.name}'), nullable=False)

    def __repr__(self):
        return f"<Student(" \
               f"id='{self.id}'," \
               f"request_type='{self.request_type}', " \
               f"url='{self.url}', "\
               f"error_code='{self.error_code}', " \
               f"ip='{self.ip}', " \
               f"file_id='{self.file_id}'" \
               f")>"
