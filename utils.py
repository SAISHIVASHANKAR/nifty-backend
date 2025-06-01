import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "nifty_stocks.db")

# Load price data from SQLite
def get_cached_df(symbol):
    conn = sqlite3.connect(DB_PATH)
    query = f"SELECT Date, Close, High, Low, Open, Volume FROM prices WHERE Symbol = '{symbol}'"
    df = pd.read_sql(query, conn, parse_dates=["Date"])
    conn.close()
    if df.empty or df.isnull().any().any():
        return None
    df.sort_values("Date", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

# Save indicator signal to SQLite
def insert_indicator_signal(symbol, indicator, signal_type, signal_value, strength, category, count):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO signals (symbol, indicator, signal_type, signal_value, strength, category, count)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (symbol, indicator, signal_type, signal_value, strength, category, count))

    conn.commit()
    conn.close()

def insert_price_data(conn, df, symbol):
    df = df.copy()
    df["Symbol"] = str(symbol)  # Ensure symbol is str
    df = df[["Symbol", "Date", "Open", "High", "Low", "Close", "Volume"]]

    # Fix for unsupported types: convert to native Python types
    df = df.astype({
        "Symbol": str,
        "Date": str,
        "Open": float,
        "High": float,
        "Low": float,
        "Close": float,
        "Volume": float
    })

    tuples = list(df.itertuples(index=False, name=None))

    try:
        with conn:
            conn.executemany("""
                INSERT INTO prices (Symbol, Date, Open, High, Low, Close, Volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, tuples)
    except Exception as e:
        print(f"❌ Insert failed for {symbol}: {e}")
