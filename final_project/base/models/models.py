from sqlalchemy import Column, INTEGER, VARCHAR, SMALLINT, DATETIME
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class UsersTest(Base):
    __tablename__ = 'test_users'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(INTEGER, nullable=False, autoincrement=True, primary_key=True)
    username = Column(VARCHAR(16), nullable=True, unique=True)
    password = Column(VARCHAR(255), nullable=False)
    email = Column(VARCHAR(64), nullable=False, unique=True)
    access = Column(SMALLINT, nullable=True)
    active = Column(SMALLINT, nullable=True)
    start_active_time = Column(DATETIME, nullable=True)

    def __repr__(self):
        return f"<test_users(" \
               f"id='{self.id}'," \
               f"username='{self.username}'," \
               f"password='{self.password}'," \
               f"email='{self.email}'," \
               f"access='{self.access}'," \
               f"active='{self.active}'," \
               f"start_active_time='{self.start_active_time}')>"
