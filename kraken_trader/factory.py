#!/bin/python

from flask import Flask, g
from werkzeug.utils import find_modules, import_string
from kraken_trader.blueprints.kraken_trader import init_db, kraken_api_importer_command
import click

_APP_NAME = 'kraken_trader'

def create_app(config=None):
    app = Flask('kraken_trader')
    app.config.from_envvar('FLASK_SETTINGS')

    # db config
    app.config.setdefault('MYSQL_PORT', 3306)
    app.config.setdefault('MYSQL_UNIX_SOCKET', None)
    app.config.setdefault('MYSQL_CONNECT_TIMEOUT', 10)
    app.config.setdefault('MYSQL_READ_DEFAULT_FILE', None)
    app.config.setdefault('MYSQL_USE_UNICODE', True)
    app.config.setdefault('MYSQL_CHARSET', 'utf8')
    app.config.setdefault('MYSQL_SQL_MODE', None)
    app.config.setdefault('MYSQL_CURSORCLASS', None)

    register_blueprints(app)
    register_cli(app)
    register_teardowns(app)

    return app


def register_blueprints(app):
    for name in find_modules(_APP_NAME + '.blueprints'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)
    return None

def register_cli(app):
    @app.cli.command('init_db')
    def init_db_command():
        init_db()

    @app.cli.command('kraken_importer')
    @click.option('--import_type', type=click.Choice(['currencies', 'values']))
    @click.option('--fiat', default='EUR')
    def kraken_importer_command(import_type, fiat):
        api_key = app.config['KRAKEN_API_KEY']
        api_secret = app.config['KRAKEN_API_SECRET']

        kraken_api_importer_command(import_type, fiat, api_key, api_secret)

def register_teardowns(app):
    @app.teardown_appcontext
    def teardown_db(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()
