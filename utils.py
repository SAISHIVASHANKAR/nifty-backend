# utils.py

import os
import sqlite3
import pandas as pd

CACHE_DIR = "/mnt/yf_cache"
DB_PATH = "nifty_stocks.db"

def get_cached_df(symbol):
    """
    Loads the cached CSV for a given stock symbol from /mnt/yf_cache.
    Returns a pandas DataFrame with parsed dates and date index.
    """
    path = os.path.join(CACHE_DIR, f"{symbol}.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing cache file for {symbol}")
    
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    return df

def load_price_data(symbol):
    """
    Loads OHLCV data for a stock symbol from the SQLite database.
    Returns a DataFrame with date index.
    """
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError("nifty_stocks.db not found")

    conn = sqlite3.connect(DB_PATH)
    query = f"""
        SELECT date, open, high, low, close, volume
        FROM price_data
        WHERE symbol = ?
        ORDER BY date ASC
    """
    df = pd.read_sql_query(query, conn, params=(symbol,))
    conn.close()

    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    return df
