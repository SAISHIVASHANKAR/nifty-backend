import sqlite3
import pandas as pd
from datetime import datetime

DB_PATH = "nifty_stocks.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def get_cached_df(symbol):
    conn = get_connection()
    query = f"""
        SELECT Date, Close, High, Low, Open, Volume
        FROM prices
        WHERE Symbol = ?
        ORDER BY Date ASC
    """
    try:
        df = pd.read_sql(query, conn, params=(symbol,), parse_dates=["Date"])
        return df
    except Exception as e:
        print(f"⚠️ Failed to load cached data for {symbol}: {e}")
        return pd.DataFrame()

def insert_into_prices_table(df, symbol):
    try:
        if df.empty:
            print(f"⚠️ Empty DataFrame, skipping insert for {symbol}")
            return False

        # Ensure proper formatting
        df = df.copy()
        df.reset_index(inplace=True)
        if "Date" not in df.columns:
            df["Date"] = df["index"]
        df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
        df["Symbol"] = symbol

        required_cols = ["Symbol", "Date", "Open", "High", "Low", "Close", "Volume"]
        df = df[required_cols]
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

        df = df[required_cols]
        df.dropna(inplace=True)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prices (
                Symbol TEXT,
                Date TEXT,
                Open REAL,
                High REAL,
                Low REAL,
                Close REAL,
                Volume REAL
            )
        """)

        df.to_sql("prices", conn, if_exists="append", index=False)
        conn.commit()
        return True
    except Exception as e:
        print(f"❌ DB insert error for {symbol}: {e}")
        return False
