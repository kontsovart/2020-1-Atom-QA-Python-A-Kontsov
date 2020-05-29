import sqlalchemy
from sqlalchemy.orm import sessionmaker


class MysqlOrmConnection:

    def __init__(self, user, password, db_name, host, port):
        self.user = user
        self.password = password
        self.db_name = db_name

        self.host = host
        self.port = port

        self.connection = self.get_connection()

        session = sessionmaker(bind=self.connection.engine, enable_baked_queries=False)
        self.session = session()

    def get_connection(self):
        engine = sqlalchemy.create_engine(
            'mysql+pymysql://{user}:{password}@{host}:{port}/{db}'.format(user=self.user,
                                                                          password=self.password,
                                                                          host=self.host,
                                                                          port=self.port,
                                                                          db=self.db_name),
            encoding='utf8'
        )

        return engine.connect()

    def execute_query(self, query):
        res = self.connection.execute(query)
        return res.fetchall()
