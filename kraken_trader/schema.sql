CREATE TABLE `user` (
    id TINYINT UNSIGNED AUTO_INCREMENT NOT NULL,
    username VARCHAR(180) NOT NULL, 
    email VARCHAR(180) NOT NULL, 
    enabled TINYINT(1) NOT NULL, 
    salt VARCHAR(255) DEFAULT NULL, 
    password VARCHAR(255) NOT NULL, 
    PRIMARY KEY(id)
) DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ENGINE = InnoDB;

CREATE TABLE crypto_currency (
    id TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE,
    exchange_currency_code VARCHAR(10) NOT NULL,
    PRIMARY KEY (id)
) DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ENGINE = InnoDB;

CREATE TABLE crypto_currency_historical_value (
    id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
    crypto_currency_id TINYINT UNSIGNED NOT NULL,
    value DECIMAL(11,6),
    created_at DATETIME,
    PRIMARY KEY (id),
    FOREIGN KEY (crypto_currency_id) REFERENCES crypto_currency(id)
) DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ENGINE = InnoDB;

CREATE TABLE transaction (
    id TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id TINYINT UNSIGNED NOT NULL,
    crypto_currency_id TINYINT UNSIGNED NOT NULL,
    units DECIMAL(11, 6),
    price DECIMAL(11, 6),
    tx_type TINYINT UNSIGNED NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (crypto_currency_id) REFERENCES crypto_currency(id)
) DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ENGINE = InnoDB;