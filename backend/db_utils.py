import mysql.connector
from models import PortfolioItem

def insert_portfolio_item(item: PortfolioItem):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Emilio0701!",
        database="portfolio_db"
    )
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

def get_all_items():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Emilio0701!",
        database="portfolio_db"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM portfolio;")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def update_portfolio_item(item_id: int, updated_item: PortfolioItem):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Emilio0701!",
        database="portfolio_db"
    )
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
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Emilio0701!",
        database="portfolio_db"
    )
    cursor = conn.cursor()
    sql = "DELETE FROM portfolio WHERE id = %s"
    cursor.execute(sql, (item_id,))
    conn.commit()
    cursor.close()
    conn.close()
