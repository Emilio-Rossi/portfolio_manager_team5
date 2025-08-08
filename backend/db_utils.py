from collections import deque
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

    # Step 1: Fetch all transactions in date order
    cursor.execute("""
        SELECT ticker, quantity, asset_type, purchase_price, purchase_date
        FROM portfolio
        ORDER BY purchase_date ASC, id ASC;
    """)
    transactions = cursor.fetchall()
    cursor.close()
    conn.close()

    # Step 2: Process FIFO per ticker
    portfolio = {}

    for tx in transactions:
        ticker = tx['ticker']
        quantity = tx['quantity']
        price = tx['purchase_price']
        asset_type = tx['asset_type']

        if ticker not in portfolio:
            portfolio[ticker] = {
                'asset_type': asset_type,
                'fifo_queue': deque(),  # stores tuples of (qty, price)
            }

        fifo = portfolio[ticker]['fifo_queue']

        if quantity > 0:
            # Buying stock → add to FIFO queue
            fifo.append((quantity, price))
        else:
            # Selling stock → remove from oldest buys
            qty_to_sell = -quantity
            while qty_to_sell > 0 and fifo:
                buy_qty, buy_price = fifo[0]
                if buy_qty > qty_to_sell:
                    fifo[0] = (buy_qty - qty_to_sell, buy_price)
                    qty_to_sell = 0
                else:
                    fifo.popleft()
                    qty_to_sell -= buy_qty

    # Step 3: Calculate remaining quantity and FIFO avg purchase price
    result = []
    for ticker, data in portfolio.items():
        fifo = data['fifo_queue']
        total_qty = sum(qty for qty, _ in fifo)
        total_cost = sum(qty * price for qty, price in fifo)
        if total_qty == 0:
            continue  # skip tickers with zero holdings

        avg_price = round(total_cost / total_qty, 2)
        result.append({
            'ticker': ticker,
            'asset_type': data['asset_type'],
            'total_quantity': total_qty,
            'avg_price': avg_price
        })

    return result
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

    cursor.execute("""
        SELECT id, purchase_date, ticker, quantity, balance
        FROM portfolio
        ORDER BY purchase_date, id;
    """)
    transactions = cursor.fetchall()
    cursor.close()
    conn.close()

    df = pd.DataFrame(transactions)
    if df.empty:
        return []

    df['purchase_date'] = pd.to_datetime(df['purchase_date'])
    tickers = sorted(df['ticker'].unique().tolist())

    # Last 7 calendar days (includes weekend)
    today = datetime.today()
    days = [(today - timedelta(days=i)).date() for i in range(6, -1, -1)]

    # Download with a buffer so we always have a prior business day
    start_buf = pd.Timestamp(days[0]) - pd.Timedelta(days=10)
    end_buf = today.date() + timedelta(days=1)  # include today if available

    raw = yf.download(
        tickers,
        start=start_buf,
        end=end_buf,
        interval="1d",
        auto_adjust=True,
        progress=False
    )

    # Normalize 'Close' to a 2D frame with all tickers as columns
    close = raw['Close'] if 'Close' in raw else pd.DataFrame(index=[], columns=tickers)
    if isinstance(close, pd.Series):  # single-ticker edge case
        close = close.to_frame(name=tickers[0])

    # Ensure all tickers exist as columns
    close = close.reindex(columns=tickers)

    daily_values = []
    for day in days:
        day_ts = pd.Timestamp(day)
        # holdings up to this calendar day
        holdings = (
            df[df['purchase_date'] <= day_ts]
            .groupby('ticker', as_index=True)['quantity']
            .sum()
        )

        equity_value = 0.0

        for ticker, qty in holdings.items():
            if qty <= 0:
                continue

            price = None
            if day == today.date():
                # Try live (intraday) for today
                try:
                    live = yf.Ticker(ticker).history(period='1d', interval='1m')
                    if not live.empty:
                        price = float(live['Close'].iloc[-1])
                except Exception:
                    price = None

                # Live failed? Use last available close up to yesterday
                if price is None or pd.isna(price):
                    hist_series = close[ticker].loc[:day_ts].dropna()
                    price = float(hist_series.iloc[-1]) if not hist_series.empty else None

                # Still nothing? Only now use the safety net for TODAY
                if price is None or pd.isna(price):
                    price = 1500.0

            else:
                # Historical day: strictly use last available close on/before that day
                hist_series = close[ticker].loc[:day_ts].dropna()
                price = float(hist_series.iloc[-1]) if not hist_series.empty else 0.0
                # Note: using 0.0 for historical missing data avoids fake spikes

            equity_value += qty * price

        # Get most recent cash balance on or before this day
        day_tx = (
            df[df['purchase_date'] <= day_ts]
            .sort_values(['purchase_date', 'id'], ascending=[False, False])
        )
        cash_balance = float(day_tx.iloc[0]['balance']) if not day_tx.empty else 10000.0

        total_value = equity_value + cash_balance
        daily_values.append({
            "date": str(day),
            "portfolio_value": round(total_value, 2),
            "equity_value": round(equity_value, 2),
            "cash_balance": round(cash_balance, 2)
        })

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
