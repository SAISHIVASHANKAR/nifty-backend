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
