# utils.py

import sqlite3
import pandas as pd

DB_FILE = "nifty_stocks.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def create_prices_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            Symbol TEXT,
            Date TEXT,
            Open REAL,
            High REAL,
            Low REAL,
            Close REAL,
            Volume REAL
        )
    ''')
    conn.commit()
    conn.close()

def insert_into_prices_table(symbol: str, df: pd.DataFrame):
    if df.empty:
        print(f"⚠️ Skipping {symbol}: DataFrame is empty")
        return

    conn = get_connection()
    df = df.copy()
    df.reset_index(inplace=True)
    df['Symbol'] = symbol
    df = df[['Symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    try:
        df.to_sql("prices", conn, if_exists="append", index=False)
        print(f"✅ {symbol} inserted: {len(df)} rows")
    except Exception as e:
        print(f"❌ DB insert error for {symbol}: {e}")
    conn.close()

def get_cached_df(symbol: str) -> pd.DataFrame:
    conn = get_connection()
    query = f"SELECT Date, Close, High, Low, Open, Volume FROM prices WHERE Symbol = ?"
    try:
        df = pd.read_sql(query, conn, params=(symbol,), parse_dates=["Date"])
        df.set_index("Date", inplace=True)
        return df
    except Exception as e:
        print(f"⚠️ Error reading {symbol} from DB: {e}")
        return pd.DataFrame()
    finally:
        conn.close()
