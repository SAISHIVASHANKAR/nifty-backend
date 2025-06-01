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

def get_cached_df(symbol):
    try:
        path = f"/mnt/yf_cache/{symbol}.csv"
        df = pd.read_csv(path, skiprows=1)

        # Rename based on available columns
        df.columns = [col.strip().split('.')[0] for col in df.columns]
        cols = df.columns.tolist()

        # Reorder to our required order
        expected = ["Date", "Open", "High", "Low", "Close", "Volume"]
        if not all(col in cols for col in expected):
            print(f"⚠️ Skipping {symbol}: Missing required columns")
            return None

        df = df[expected]
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.dropna().sort_values("Date").reset_index(drop=True)

        return df
    except Exception as e:
        print(f"❌ Failed to load CSV for {symbol}: {e}")
        return None
