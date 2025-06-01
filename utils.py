import sqlite3
import pandas as pd

# Create the DB schema if needed
def init_db():
    conn = sqlite3.connect("nifty_stocks.db")
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
        );
    """)
    conn.commit()
    conn.close()

# Main insert function
def insert_into_prices_table(df, symbol):
    if df is None or df.empty:
        print(f"⚠️ Skipped DB insert for {symbol}: Empty DataFrame.")
        return

    try:
        df = df.copy()
        df["Symbol"] = symbol  # Ensure symbol column exists
        df["Date"] = pd.to_datetime(df["Date"]).dt.strftime('%Y-%m-%d')  # Normalize date format

        expected_cols = ["Date", "Open", "High", "Low", "Close", "Volume", "Symbol"]
        df = df[expected_cols]  # Enforce order

        conn = sqlite3.connect("nifty_stocks.db")
        df.to_sql("prices", conn, if_exists="append", index=False)
        conn.close()
        print(f"✅ DB insert complete for {symbol} ({len(df)} rows)")

    except Exception as e:
        print(f"❌ Failed to insert {symbol} into DB: {e}")
