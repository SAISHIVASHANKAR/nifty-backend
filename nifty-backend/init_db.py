# init_db.py
import sqlite3

DB_PATH = "nifty_stocks.db"

def init_prices_table():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prices (
                date TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER,
                symbol TEXT
            )
        """)
        conn.commit()
        conn.close()
        print("✅ 'prices' table created or verified successfully.")
    except Exception as e:
        print(f"❌ Error initializing DB: {e}")

if __name__ == "__main__":
    init_prices_table()
