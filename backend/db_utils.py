from datetime import datetime, timedelta
import os
import mysql.connector
from dotenv import load_dotenv
import pandas as pd
from models import PortfolioItem
import yfinance as yf

# Load environment variables
load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST", "localhost")
db_name = os.getenv("DB_NAME", "portfolio_db")

# Helper function to create a DB connection
def get_connection():
    return mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

def insert_portfolio_item(item: PortfolioItem):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO portfolio (ticker, quantity, asset_type, purchase_price, purchase_date,balance)
        VALUES (%s, %s, %s, %s, %s,%s)
    """
    values = (
        item.ticker,
        item.quantity,
        item.asset_type,
        item.purchase_price,
        item.purchase_date,
        item.balance
    )
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()

def view_portfolios():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
            SELECT
            ticker,
            ANY_VALUE(asset_type) AS asset_type,
            SUM(quantity) AS total_quantity,
            CASE
                WHEN SUM(CASE WHEN quantity > 0 THEN quantity ELSE 0 END) > 0
                THEN ROUND(
                    SUM(CASE WHEN quantity > 0 THEN purchase_price * quantity ELSE 0 END)
                    / SUM(CASE WHEN quantity > 0 THEN quantity ELSE 0 END),
                    2
                )
                ELSE 0
            END AS avg_price
            FROM portfolio
            GROUP BY ticker
            HAVING total_quantity>0;
            """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
def view_purchases():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
            SELECT *
            FROM portfolio;
            """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
def get_net_quantity(ticker):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
            SELECT 
                COALESCE(sum(quantity),0) AS net_quantity
            FROM portfolio
            where ticker=%s;
            """,(ticker, ))
    results = cursor.fetchone()
    cursor.close()
    conn.close()
    return results['net_quantity'] if results else 0
def get_current_balance():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT balance
            FROM portfolio
            ORDER BY purchase_date desc,id DESC
            LIMIT 1;
        """)
        result = cursor.fetchone()
        return result[0] if result else 10000  # Return numeric value
    finally:
        cursor.close()
        conn.close()

def get_1week_portfolio_value():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get all transactions
    cursor.execute("SELECT id,purchase_date, ticker, quantity, balance FROM portfolio ORDER BY purchase_date;")
    transactions = cursor.fetchall()

    df = pd.DataFrame(transactions)
    df['purchase_date'] = pd.to_datetime(df['purchase_date'])
    tickers = df['ticker'].unique().tolist()

    # Get last 7 days
    today = datetime.today()
    days = [(today - timedelta(days=i)).date() for i in range(6, -1, -1)]

    # Download historical prices for last 7 days
    prices = yf.download(tickers, start=days[0], end=today, interval="1d")['Close']

    daily_values = []
    for day in days:
        # Equity Holdings up to this day
        holdings = df[df['purchase_date'] <= pd.Timestamp(day)].groupby('ticker')['quantity'].sum()

        # Calculate equity value
        equity_value = 0
        for ticker, qty in holdings.items():
            if qty > 0 and ticker in prices.columns:
                if pd.Timestamp(day) in prices.index:
                    price = prices.loc[pd.Timestamp(day), ticker]
                else:
                    price = prices[ticker].ffill().iloc[-1]
                equity_value += qty * price

        # Get most recent cash balance before or on this day
        day_transactions = df[df['purchase_date'] <= pd.Timestamp(day)].sort_values(by=['purchase_date', 'id'], ascending=[False, False])
        cash_balance = float(day_transactions.iloc[0]['balance']) if not day_transactions.empty else 10000.0
        print(cash_balance)

        total_value = equity_value + cash_balance
        daily_values.append({
            "date": str(day),
            "portfolio_value": round(total_value, 2),
            "equity_value": round(equity_value, 2),
            "cash_balance": round(cash_balance, 2)
        })

    cursor.close()
    conn.close()
    return daily_values
def update_portfolio_item(item_id: int, updated_item: PortfolioItem):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        UPDATE portfolio
        SET ticker = %s, quantity = %s, asset_type = %s,
            purchase_price = %s, purchase_date = %s
        WHERE id = %s
    """
    values = (
        updated_item.ticker,
        updated_item.quantity,
        updated_item.asset_type,
        updated_item.purchase_price,
        updated_item.purchase_date,
        item_id
    )
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()

def delete_portfolio_item(item_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM portfolio WHERE id = %s"
    cursor.execute(sql, (item_id,))
    conn.commit()
    cursor.close()
    conn.close()
