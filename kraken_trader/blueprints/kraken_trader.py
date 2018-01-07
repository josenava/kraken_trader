from flask import Blueprint, g, current_app, render_template
from kraken_trader.components.db.db_connector import DbConnector
from kraken_trader.components.logger.query_logger import QueryLogger
from kraken_trader.components.kraken_importer import KrakenImporter
from kraken_trader.components.crypto_currency_service import CryptoCurrencyService
import _mysql_exceptions

bp = Blueprint('kraken_trader', __name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = DbConnector(QueryLogger(current_app.logger, current_app.config['QUERY_LOG_FILE']))
    return db


def init_db():
    try:
        db_connector = get_db()
        with current_app.open_resource('schema.sql', mode='r') as f:
            query = f.read()

        db_connector.execute(query)
    except _mysql_exceptions.OperationalError as error:
        print('Something went wrong: {}'.format(error))


def kraken_api_importer_command(import_type, fiat, api_key, api_secret):
    importer = KrakenImporter(api_key, api_secret, get_db())
    if import_type == 'currencies':
        return importer.currencies()
    elif import_type == 'values':
        return importer.values(fiat)
    else:
        print('Wrong option')
        return 1

@bp.route('/')
def show_prices():
    crypto_currency_service = CryptoCurrencyService(get_db())
    (updated_at, last_values) = crypto_currency_service.get_last_values()

    return render_template('show_prices.html', updated_at=updated_at,
                           crypto_currencies=last_values)
