[WIP]Kraken trader tool
=======================

Flask app to check your kraken portfolio and trade.

Install guide:

1. `pip install .`
2. `mv .env.sample .env` And check the content so you modify it with your parameters
3. Add your config parameters to `config.cfg`
4. Run `flask init_db`
5. Run `flask kraken_importer --import_type=currencies`
6. Run `flask kraken_importer --import_type=values`
7. Run `flask run` to see your application.

Commands:

- Create a database and run the following command to create the tables.
`flask init_db`

- Import the currencies from kraken
`flask kraken_importer --import_type=currencies`

- Import currency values from kraken
`flask kraken_importer --import_type=values`



Stack:

- Python 3.6
- Flask
- MySQL 5.7