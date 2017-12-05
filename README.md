[WIP]Kraken trader tool
=======================

Flask app to check your kraken portfolio and trade.

Install guide:

`pip install .`

Commands:

- Create a database and run the following command to create the tables.
`flask init_db`

- Import the currencies from kraken
`flask kraken_importer_cli --import_type=currencies`

- Import currency values from kraken
`flask kraken_importer_cli --import_type=values`



Stack:

- Python 3.6
- Flask
- MySQL 5.7