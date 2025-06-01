
# run_indicators.py

import os
import sqlite3
import pandas as pd
from indicators import compute_all_indicators
from utils import get_cached_df
from stocks import STOCKS

DB_PATH = "indicator_signals.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            symbol TEXT PRIMARY KEY,
            trend INTEGER,
            momentum INTEGER,
            volume INTEGER,
            volatility INTEGER,
            support_resistance INTEGER
        )
    """)
    conn.commit()
    conn.close()

def save_signal_to_db(symbol, signal_tuple):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO signals
        (symbol, trend, momentum, volume, volatility, support_resistance)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (symbol, *signal_tuple))
    conn.commit()
    conn.close()

def process_stock(symbol):
    try:
        df = get_cached_df(symbol)
        signal_tuple = compute_all_indicators(symbol, df)
        if signal_tuple:
            save_signal_to_db(symbol, signal_tuple)
            print(f"âœ… Processed: {symbol}")
        else:
            print(f"âš ï¸ Skipped {symbol}: No data or failed indicator computation.")
    except Exception as e:
        print(f"âŒ Error processing {symbol}: {e}")

def main():
    print("Running indicators and saving signals to indicator_signals.db")
    init_db()
    for symbol in list(STOCKS.keys())[:300]:  # test mode limit, remove [:300] for full run
        print(f"ðŸ“Š Processing: {symbol}")
        process_stock(symbol)

if __name__ == "__main__":
    main()
