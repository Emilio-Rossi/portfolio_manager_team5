import mysql.connector

def initialize_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password_here",  # Replace with own password
    )
    cursor = conn.cursor()

    # Create the database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS portfolio_db;")
    cursor.execute("USE portfolio_db;")

    # Create the table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS portfolio (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ticker VARCHAR(10) NOT NULL,
            quantity INT NOT NULL,
            asset_type VARCHAR(20) NOT NULL,
            purchase_price FLOAT NOT NULL,
            purchase_date DATE
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    initialize_database()
