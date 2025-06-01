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

def insert_indicator_signal(symbol, trend, momentum, volume, volatility, support_resistance, count):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS signals (
                symbol TEXT PRIMARY KEY,
                trend INTEGER,
                momentum INTEGER,
                volume INTEGER,
                volatility INTEGER,
                support_resistance INTEGER,
                count INTEGER
            )
        """)
        c.execute("""
            INSERT OR REPLACE INTO signals (symbol, trend, momentum, volume, volatility, support_resistance, count)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (symbol, trend, momentum, volume, volatility, support_resistance, count))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"❌ Failed to insert signal for {symbol}: {e}")
