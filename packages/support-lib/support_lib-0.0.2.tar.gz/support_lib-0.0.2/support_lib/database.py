# import cx_Oracle
import oracledb as cx_Oracle
import os


class Database:
    """
    Oracle Database Utils
    CONSTRUCTOR:
        PARAMS:
            username : [string]
            password : [string]
            host : [string]
            port : [string]
            service : [string]
            logger : [object]
    METHODS:
        connect : returns Database connection
        disconnect : closes the Database connection
        get_Data : Gets data from Database
            PARAMS : query : [string]
            RETURNS : Tuple or False [Boolean]
        update_data : Update or Insert data into Database
            PARAMS : query : [string]
            RETURNS : 'Updated' [string] or 'Error' with error message [string]
    """

    def __init__(self, username, password, host, port, service, logger):

        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.service = service
        self.connection = None
        self.cursor = None
        self.logger = logger

    def OutputTypeHandler(self, cursor, name, defaultType, size, precision, scale):
        if defaultType == cx_Oracle.CLOB:
            return cursor.var(cx_Oracle.LONG_STRING, arraysize=cursor.arraysize)
        elif defaultType == cx_Oracle.BLOB:
            return cursor.var(cx_Oracle.LONG_BINARY, arraysize=cursor.arraysize)

    def connect(self):
        """ we start the connection to the database """

        # You can set these in system variables but just in case you didnt
        os.putenv('ORACLE_HOME', '/opt/oracle/instantclient')
        os.putenv('LD_LIBRARY_PATH', '/opt/oracle/instantclient')

        connection_string = self.username + '/' + self.password + '@' + self.host + ':' + self.port + '/' + self.service

        try:
            self.connection = cx_Oracle.connect(connection_string)
            self.logger.info(f'Connected to {self.service} on {self.host} as user {self.username}')
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            if error.code == 1017:
                self.logger.error.error('Please check your oracle credentials.')
            else:
                self.logger.error('Database connection error: %s'.format(e))
                # Very important part!
            raise

        self.cursor = self.connection.cursor()
        self.connection.autocommit = 1
        return self.connection

    def disconnect(self):
        """ we close the connection to the database """

        self.cursor.close()
        self.connection.close()

    def get_data(self, query):
        """ Get data from database with passed in query """
        self.logger.info('SQL - {}'.format(query))
        try:
            self.cursor.execute(query)
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            if error.code == 955:
                self.logger.error('Table already exists')
            elif error.code == 1031:
                self.logger.error("Insufficient privileges")
                self.logger.error(error.code)
                self.logger.error(error.message)
                self.logger.error(error.context)
            raise

        data = self.cursor.fetchall()
        if len(data) > 0:
            return data
        else:
            return False

    def update_data(self, query):
        """ Update date in database with passed in query """

        self.logger.info('SQL - {}'.format(query))
        try:
            self.cursor.execute(query)
            return 'Updated'
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            if error.code == 955:
                self.logger.error('Table already exists')
            elif error.code == 1031:
                self.logger.error("Insufficient privileges")
                self.logger.error(error.code)
                self.logger.error(error.message)
                self.logger.error(error.context)
                return 'Error {}'.format(error)
            raise
