#!/bin/python

import _mysql_exceptions
import click
from kraken_trader.components.kraken_importer import KrakenImporter
from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_envvar('FLASK_SETTINGS')
mysql = MySQL(app)


@app.cli.command('init_db')
def initdb_command():
    try:
        cursor = mysql.connection.cursor()
        with app.open_resource('schema.sql', mode='r') as f:
            query = f.read()
            print("'Running query: {}'".format(query))

        cursor.execute(query)
    except _mysql_exceptions.OperationalError as error:
        print('Something went wrong: {}'.format(error))
    finally:
        cursor.close()


@app.cli.command('kraken_importer_cli')
@click.option('--import_type', type=click.Choice(['currencies', 'values']))
@click.option('--fiat', default='EUR')
def kraken_importer_command(import_type, fiat):
    importer = KrakenImporter(
        app.config['KRAKEN_API_KEY'], app.config['KRAKEN_API_SECRET'], mysql)
    if import_type == 'currencies':
        return importer.currencies()
    elif import_type == 'values':
        return importer.values(fiat)
    else:
        print('Wrong option')
        return 1

def main():
    app.run()

if __name__ == '__main__':
    main()
