# utils.py

import pandas as pd
import sqlite3

CACHE_DIR = "/mnt/yf_cache"
DB_PATH = "indicator_signals.db"

def load_price_data(symbol):
    path = f"{CACHE_DIR}/{symbol}.csv"
    try:
        df = pd.read_csv(path)
        df.columns = [col.split('.')[0] for col in df.columns]  # Removes '.NS' junk
        df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]  # Select only valid columns
        df = df.dropna()
        df["Date"] = pd.to_datetime(df["Date"])
        df.set_index("Date", inplace=True)

        for col in ["Open", "High", "Low", "Close", "Volume"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        return df
    except Exception as e:
        print(f"❌ Failed to load data for {symbol}: {e}")
        return None

def insert_indicator_signal(conn, symbol, trend, momentum, volume, volatility, support_resistance, count):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO signals (symbol, trend, momentum, volume, volatility, support_resistance, count)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            str(symbol),
            int(trend),
            int(momentum),
            int(volume),
            int(volatility),
            int(support_resistance),
            int(count)
        ))
        conn.commit()
    except Exception as e:
        print(f"❌ Failed to insert signal for {symbol}: {e}")

import pandas as pd

import pandas as pd
import os

def get_cached_df(symbol):
    path = f"/mnt/yf_cache/{symbol}.csv"
    if not os.path.exists(path):
        return None

    try:
        df = pd.read_csv(path)

        # Drop second row if it contains repeated headers
        if df.iloc[0].str.contains(symbol).sum() >= 3:
            df = df[1:]

        # Coerce numeric conversion
        cols = ['Close', 'High', 'Low', 'Open', 'Volume']
        for col in cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df.dropna(subset=cols, inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    except Exception as e:
        print(f"Error loading {symbol}.csv: {e}")
        return None
