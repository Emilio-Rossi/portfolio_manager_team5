import os
import mysql.connector
from dotenv import load_dotenv
from models import PortfolioItem

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
        INSERT INTO portfolio (ticker, quantity, asset_type, purchase_price, purchase_date)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (
        item.ticker,
        item.quantity,
        item.asset_type,
        item.purchase_price,
        item.purchase_date
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
                SUM(quantity) AS total_quantity,
                ROUND(SUM(purchase_price * quantity) / SUM(quantity), 2) AS avg_price
            FROM portfolio
            GROUP BY ticker;
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
                COALESCE(sum(quantity),0) AS net_quantity,
            FROM portfolio
            where ticker=%s;
            """,(ticker, ))
    results = cursor.fetchone()
    cursor.close()
    conn.close()
    return results

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
