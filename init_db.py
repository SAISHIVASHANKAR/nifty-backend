# init_db.py
import sqlite3

DB_PATH = "nifty_stocks.db"

def init_prices_table():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prices (
                Date TEXT,
                Open REAL,
                High REAL,
                Low REAL,
                Close REAL,
                Volume INTEGER,
                Symbol TEXT
            )
        """)
        conn.commit()
        conn.close()
        print("✅ 'prices' table created or verified successfully.")
    except Exception as e:
        print(f"❌ Error initializing DB: {e}")

if __name__ == "__main__":
    init_prices_table()
