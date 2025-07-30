
CREATE DATABASE IF NOT EXISTS portfolio_db;

USE portfolio_db;

CREATE TABLE IF NOT EXISTS portfolio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    quantity INT NOT NULL,
    asset_type VARCHAR(20) NOT NULL,
    purchase_price FLOAT NOT NULL,
    purchase_date DATE
);

