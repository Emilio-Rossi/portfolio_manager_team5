
CREATE DATABASE IF NOT EXISTS portfolio_db;

USE portfolio_db;
DROP TABLE IF EXISTS portfolio;

CREATE TABLE IF NOT EXISTS portfolio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    quantity INT NOT NULL,
    asset_type VARCHAR(20) NOT NULL,
    purchase_price FLOAT NOT NULL,
    purchase_date DATE,
    balance FLOAT NOT NULL
);

USE portfolio_db;
-- ===== Day 1: 2025-08-02 =====
-- Start: $10,000
-- Buy AAPL 10 @ $200 → cost $2,000 → balance $8,000
INSERT INTO portfolio (ticker, quantity, asset_type, purchase_price, purchase_date, balance)
VALUES ('AAPL', 10, 'equity', 200.0, '2025-08-02', 8000.0);

-- Buy MSFT 5 @ $500 → cost $2,500 → balance $5,500
INSERT INTO portfolio (ticker, quantity, asset_type, purchase_price, purchase_date, balance)
VALUES ('MSFT', 5, 'equity', 500.0, '2025-08-02', 5500.0);

-- Buy AMZN 4 @ $200 → cost $800 → balance $4,700
INSERT INTO portfolio (ticker, quantity, asset_type, purchase_price, purchase_date, balance)
VALUES ('AMZN', 4, 'equity', 200.0, '2025-08-02', 4700.0);

-- ===== Day 2: 2025-08-03 =====
-- Buy TSLA 5 @ $300 → cost $1,500 → balance $3,200
INSERT INTO portfolio (ticker, quantity, asset_type, purchase_price, purchase_date, balance)
VALUES ('TSLA', 5, 'equity', 300.0, '2025-08-03', 3200.0);

-- Buy META 2 @ $740 → cost $1,480 → balance $1,720
INSERT INTO portfolio (ticker, quantity, asset_type, purchase_price, purchase_date, balance)
VALUES ('META', 2, 'equity', 740.0, '2025-08-03', 1720.0);

-- Buy GOOG 3 @ $180 → cost $540 → balance $1,180
INSERT INTO portfolio (ticker, quantity, asset_type, purchase_price, purchase_date, balance)
VALUES ('GOOG', 3, 'equity', 180.0, '2025-08-03', 1180.0);

-- ===== Day 3: 2025-08-04 =====
-- Sell 3 AAPL @ $155 → gain $465 → balance $1,645
INSERT INTO portfolio (ticker, quantity, asset_type, purchase_price, purchase_date, balance)
VALUES ('AAPL', -3, 'equity', 155.0, '2025-08-04', 1645.0);

-- Buy PYPL 8 @ $70 → cost $560 → balance $1,085
INSERT INTO portfolio (ticker, quantity, asset_type, purchase_price, purchase_date, balance)
VALUES ('PYPL', 8, 'equity', 70.0, '2025-08-04', 1085.0);

-- Buy PLTR 10 @ $18 → cost $180 → balance $905
INSERT INTO portfolio (ticker, quantity, asset_type, purchase_price, purchase_date, balance)
VALUES ('PLTR', 10, 'equity', 18.0, '2025-08-04', 905.0);

-- ===== Day 4: 2025-08-05 =====
-- Buy AAPL 2 @ $160 → cost $320 → balance $585
INSERT INTO portfolio (ticker, quantity, asset_type, purchase_price, purchase_date, balance)
VALUES ('AAPL', 2, 'equity', 160.0, '2025-08-05', 585.0);

-- Buy QQQ 1 @ $370 → cost $370 → balance $215
INSERT INTO portfolio (ticker, quantity, asset_type, purchase_price, purchase_date, balance)
VALUES ('QQQ', 1, 'etf', 370.0, '2025-08-05', 215.0);
