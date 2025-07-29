# Backend Module - Portfolio Manager

This folder contains backend scripts for managing the user's investment portfolio.

## Contents
- `db_utils.py`: Contains all database CRUD operations (Insert, Retrieve, Update, Delete).

## Database
- MySQL database: `portfolio_db`
- Table: `portfolio`

### Table schema
- `id`: INT, PRIMARY KEY, AUTO_INCREMENT
- `ticker`: VARCHAR
- `quantity`: INT
- `asset_type`: VARCHAR (e.g., "equity", "bond", "cash")
- `purchase_price`: FLOAT
- `purchase_date`: DATE

## Notes
- Ensure MySQL is running locally.
- Update credentials in `db_utils.py` if needed.
