#!/bin/python
import datetime
import krakenex
import _mysql_exceptions
from requests.exceptions import HTTPError

class KrakenImporter():
    def __init__(self, api_key, api_secret, db):
        self.kraken_api = krakenex.API(api_key, api_secret)
        self.db_connection = db.connection
    
    def currencies(self):
        try:
            response = self.kraken_api.query_public('AssetPairs')
            db_cursor = self.db_connection.cursor()
            query_params = [
                (crypto_currency_meta_data['base'],
                 crypto_currency_code,
                 crypto_currency_meta_data['quote'])
                for crypto_currency_code, crypto_currency_meta_data in response['result'].items()
            ]
            
            query = self.__build_insert_crypto_currency_query()
            db_cursor.executemany(query, query_params)
            self.db_connection.commit()
        except HTTPError as http_error:
            print('The API raised the following http_error: {}'.format(http_error))
        except _mysql_exceptions.DatabaseError as db_error:
            print('The database threw the following error: {}'.format(db_error))

    def values(self, fiat):
        try:
            currency_pairs = self.__get_fiat_currency_pairs(fiat)
            pair_codes = ','.join(currency_pairs.keys())

            current_values = self.kraken_api.query_public(
                'Ticker', {'pair': pair_codes})
            
            query_params = [
                (currency_pairs[crypto_currency],
                 data['c'][0], datetime.datetime.now())
                for crypto_currency, data in current_values['result'].items()
            ]
            
            query = self.__build_insert_crypto_currency_historical_value_query()
            db_cursor = self.db_connection.cursor()

            db_cursor.executemany(query, query_params)
            self.db_connection.commit()
        except HTTPError as http_error:
            print('The API returned the following error: {}'.format(http_error))
        except _mysql_exceptions.DatabaseError as db_error:
            print('The database threw the following error: {}'.format(db_error))



    def __get_fiat_currency_pairs(self, fiat):
        """
        For testing purposes we exclude currencies like *.d
        """
        try:
            select_query = '''
                SELECT code, id FROM crypto_currency 
                WHERE exchange_currency_code LIKE '%{}%'
                AND code NOT LIKE '%.d%'
            '''.format(fiat)

            db_cursor = self.db_connection.cursor()
            db_cursor.execute(select_query)
            
            return dict(db_cursor.fetchall())
        except _mysql_exceptions.DatabaseError as error:
            print('Something went wrong, please check: {}'.format(error))

    def __build_insert_crypto_currency_historical_value_query(self):
        return '''
            INSERT INTO crypto_currency_historical_value (crypto_currency_id, value, created_at)
            VALUES (%s, %s, %s)
            '''

    def __build_insert_crypto_currency_query(self):
        return '''
            INSERT INTO crypto_currency (name, code, exchange_currency_code)
            VALUES (%s, %s, %s)
        '''
