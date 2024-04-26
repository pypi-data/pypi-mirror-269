import mysql.connector as mariadb


class Database:

    def __init__(self, username, password, host, port, database, logger):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.db = None
        self.cursor = None
        self.logger = logger

    def connect(self):
        try:
            self.db = mariadb.connect(user=self.username,
                                      password=self.password,
                                      database=self.database,
                                      host=self.host)
        except Exception as e:
            return 'Unable to connect', e

        self.cursor = self.db.cursor()

        return 'Connected'

    def get_data(self, sql):
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    def update_data(self, sql):
        self.cursor.execute(sql)
        return 'Updated'

    def disconnect(self):
        self.db.commit()
        self.db.close()
