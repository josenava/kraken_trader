from flask_mysqldb import MySQL

class DbConnector(MySQL):
    def __init__(self, connection_params, logger=None):
        super().__init__(connection_params)
        # self.logger = logger
        self._cursor = None

    def execute(self, query):
        '''
        Logs the query and executes it
        '''
        # self.logger.debug(query)

        return self.cursor.execute(query)

    def executemany(self, query, query_params):
        '''
        Logs executemany query and runs it
        '''
        # self.logger.debug(query)

        return self.cursor.executemany(query, query_params)

    def close(self):
        '''
        Closes the connection if the cursor was created
        '''
        return self.cursor.close()
    
    @property
    def cursor(self):
        if self._cursor is None:
            self.connection.autocommit(True)
            self._cursor = self.connection.cursor()
        return self._cursor