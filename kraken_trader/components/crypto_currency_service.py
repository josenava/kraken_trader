#!/bin/python

class CryptoCurrencyService():
    
    def __init__(self, db_connection):
        self.db_connection = db_connection
    
    def get_last_values(self):
        query = self.__build_select_last_values_query()
        self.db_connection.execute(query)

        return self.__parse_last_values(self.db_connection.cursor.fetchall())
    
    def __build_select_last_values_query(self):
        return '''
SELECT c.name AS 'crypto_currency_name', chv.value AS 'crypto_currency_value', chv.created_at AS 'last_updated_at' FROM crypto_currency c
INNER JOIN crypto_currency_historical_value chv ON c.id = chv.crypto_currency_id
INNER JOIN (SELECT MAX(created_at) as max_created_at, crypto_currency_id AS max_crypto_id FROM crypto_currency_historical_value GROUP BY crypto_currency_id ) max_chv
ON max_chv.max_crypto_id = chv.crypto_currency_id
WHERE chv.created_at = max_chv.max_created_at
GROUP BY c.id
ORDER BY c.id ASC
        '''

    def __parse_last_values(self, values):
        return (
            values[0][2],
            {name: value for name, value, created_at in values}
        )
        