import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def initialize_database():
    try:
        # Read from .env
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST", "localhost")
        db_name = os.getenv("DB_NAME", "portfolio_db")

        # Connect without specifying database (to create it first)
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password
        )
        cursor = conn.cursor()

        # Create database if not exists
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
        cursor.execute(f"USE {db_name};")

        # Create table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS portfolio (
                id INT AUTO_INCREMENT PRIMARY KEY,
                ticker VARCHAR(10) NOT NULL,
                quantity INT NOT NULL,
                asset_type VARCHAR(20) NOT NULL,
                purchase_price FLOAT NOT NULL,
                purchase_date DATE,
                balance FLOAT NOT NULLL
            );
        """)

        conn.commit()
       
        print(f"✅ Database '{db_name}' initialized successfully.")

    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    initialize_database()
