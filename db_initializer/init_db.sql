
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
-- Buy AAPL 10 @ $150 → cost $1,500 → balance $8,500
INSERT INTO portfolio (ticker, quantity, asset_type, purchase_price, purchase_date, balance)
VALUES ('AAPL', 10, 'stock', 150.0, '2025-08-02', 8500.0);

-- Buy MSFT 5 @ $300 → cost $1,500 → balance $7,000
INSERT INTO portfolio (ticker, quantity, asset_type, purchase_price, purchase_date, balance)
VALUES ('MSFT', 5, 'stock', 300.0, '2025-08-02', 7000.0);

-- ===== Day 2: 2025-08-03 =====
-- Buy TSLA 5 @ $200 → cost $1,000 → balance $6,000
INSERT INTO portfolio (ticker, quantity, asset_type, purchase_price, purchase_date, balance)
VALUES ('TSLA', 5, 'stock', 200.0, '2025-08-03', 6000.0);

-- Buy META 4 @ $350 → cost $1,400 → balance $4,600
INSERT INTO portfolio (ticker, quantity, asset_type, purchase_price, purchase_date, balance)
VALUES ('META', 4, 'stock', 350.0, '2025-08-03', 4600.0);

-- ===== Day 3: 2025-08-04 =====
-- Sell 3 AAPL @ $155 → gain $465 → balance $5,065
INSERT INTO portfolio (ticker, quantity, asset_type, purchase_price, purchase_date, balance)
VALUES ('AAPL', -3, 'stock', 155.0, '2025-08-04', 5065.0);

-- Buy PYPL 8 @ $70 → cost $560 → balance $4,505
INSERT INTO portfolio (ticker, quantity, asset_type, purchase_price, purchase_date, balance)
VALUES ('PYPL', 8, 'stock', 70.0, '2025-08-04', 4505.0);

-- ===== Day 4: 2025-08-05 =====
-- Buy AAPL 2 @ $160 → cost $320 → balance $4,185
INSERT INTO portfolio (ticker, quantity, asset_type, purchase_price, purchase_date, balance)
VALUES ('AAPL', 2, 'stock', 160.0, '2025-08-05', 4185.0);

-- Buy TSLA 3 @ $210 → cost $630 → balance $3,555
INSERT INTO portfolio (ticker, quantity, asset_type, purchase_price, purchase_date, balance)
VALUES ('TSLA', 3, 'stock', 210.0, '2025-08-05', 3555.0);

-- ===== Day 5: 2025-08-06 =====
-- Sell 1 TSLA @ $215 → gain $215 → balance $3,770
INSERT INTO portfolio (ticker, quantity, asset_type, purchase_price, purchase_date, balance)
VALUES ('TSLA', -1, 'stock', 215.0, '2025-08-06', 3770.0);

-- Sell 2 MSFT @ $310 → gain $620 → balance $4,390
INSERT INTO portfolio (ticker, quantity, asset_type, purchase_price, purchase_date, balance)
VALUES ('MSFT', -2, 'stock', 310.0, '2025-08-06', 4390.0);

-- ===== Day 6: 2025-08-07 =====
-- Buy META 2 @ $355 → cost $710 → balance $3,680
INSERT INTO portfolio (ticker, quantity, asset_type, purchase_price, purchase_date, balance)
VALUES ('META', 2, 'stock', 355.0, '2025-08-07', 3680.0);

-- Sell 2 PYPL @ $75 → gain $150 → balance $3,830
INSERT INTO portfolio (ticker, quantity, asset_type, purchase_price, purchase_date, balance)
VALUES ('PYPL', -2, 'stock', 75.0, '2025-08-07', 3830.0);

-- ===== Day 7: 2025-08-08 =====
-- Buy AAPL 1 @ $165 → cost $165 → balance $3,665
INSERT INTO portfolio (ticker, quantity, asset_type, purchase_price, purchase_date, balance)
VALUES ('AAPL', 1, 'stock', 165.0, '2025-08-08', 3665.0);

-- Buy MSFT 1 @ $305 → cost $305 → balance $3,360
INSERT INTO portfolio (ticker, quantity, asset_type, purchase_price, purchase_date, balance)
VALUES ('MSFT', 1, 'stock', 305.0, '2025-08-08', 3360.0);
