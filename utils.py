import os
import sqlite3
import pandas as pd
from datetime import datetime

# Path to the cached EOD data folder (update if you mounted EBS elsewhere)
CACHE_DIR = "/mnt/yf_cache"

# Path to the SQLite database where signal results are saved
SIGNAL_DB_PATH = os.path.join(os.getcwd(), "indicator_signals.db")

# Load cached price data as DataFrame for a given stock symbol
def get_cached_df(symbol):
    path = os.path.join(CACHE_DIR, f"{symbol}.csv")
    if not os.path.exists(path):
        return None
    try:
        df = pd.read_csv(path)
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        df.sort_index(inplace=True)
        return df
    except Exception as e:
        print(f"[ERROR] Failed to load {symbol}.csv: {e}")
        return None

# Save signal results into SQLite table
def save_signals_to_db(signal_data):
    conn = sqlite3.connect(SIGNAL_DB_PATH)
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS signals (
            symbol TEXT PRIMARY KEY,
            trend INTEGER,
            momentum INTEGER,
            volume INTEGER,
            volatility INTEGER,
            support_resistance INTEGER,
            last_updated TEXT
        )
    ''')

    # Insert or update each row
    for row in signal_data:
        cursor.execute('''
            INSERT OR REPLACE INTO signals
            (symbol, trend, momentum, volume, volatility, support_resistance, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['symbol'],
            row['trend'],
            row['momentum'],
            row['volume'],
            row['volatility'],
            row['support_resistance'],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

    conn.commit()
    conn.close()

# Load signal data from DB (used by app.py)
def load_signals():
    if not os.path.exists(SIGNAL_DB_PATH):
        print("Signal DB not found.")
        return []

    conn = sqlite3.connect(SIGNAL_DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT symbol, trend, momentum, volume, volatility, support_resistance FROM signals")
        rows = cursor.fetchall()
        data = [
            {
                "symbol": row[0],
                "trend": row[1],
                "momentum": row[2],
                "volume": row[3],
                "volatility": row[4],
                "support_resistance": row[5],
            }
            for row in rows
        ]
        return data
    except sqlite3.OperationalError as e:
        print(f"[ERROR] SQLite issue: {e}")
        return []
    finally:
        conn.close()
