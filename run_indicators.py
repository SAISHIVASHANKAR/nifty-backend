# run_indicators.py

import os
import sqlite3
import pandas as pd
from indicators import compute_all_indicators
from utils import get_cached_df
from stocks import STOCKS

DB_PATH = "indicator_signals.db"

def load_signals():
    return sqlite3.connect(DB_PATH)

def process_stock(symbol, filepath):
    try:
        df = pd.read_csv(filepath)

        # ✅ Convert critical columns to numeric
        for col in ["Open", "High", "Low", "Close", "Adj Close", "Volume"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        df.dropna(subset=["Close"], inplace=True)

        if len(df) < 30:
            print(f"⏩ Skipping {symbol}: Not enough data")
            return None

        return compute_all_indicators(symbol, df)

    except Exception as e:
        print(f"❌ Error processing {symbol}: {e}")
        return None

def main():
    conn = load_signals()
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS signals")
    cursor.execute("""
        CREATE TABLE signals (
            symbol TEXT PRIMARY KEY,
            trend INTEGER,
            momentum INTEGER,
            volume INTEGER,
            volatility INTEGER,
            support_resistance INTEGER
        )
    """)

    for symbol in STOCKS:
        print(f"📊 Processing: {symbol}")
        filepath = f"/mnt/yf_cache/{symbol}.csv"

        if not os.path.exists(filepath):
            print(f"⏩ Skipping {symbol}: No cached file")
            continue

        result = process_stock(symbol, filepath)
        if result:
            cursor.execute("""
                INSERT INTO signals VALUES (?, ?, ?, ?, ?, ?)
            """, (symbol, *result))

    conn.commit()
    conn.close()
    print("✅ All signals computed and saved to indicator_signals.db")

if __name__ == "__main__":
    main()
