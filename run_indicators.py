# run_indicators.py

import sqlite3
import pandas as pd
from indicators import compute_all_indicators
from utils import get_cached_df
from stocks import STOCKS

def run_all_indicators():
    try:
        conn = sqlite3.connect("nifty_stocks.db")
        cursor = conn.cursor()

        print(f"📊 Total stocks: {len(STOCKS)}")
        for i, symbol in enumerate(STOCKS.keys(), 1):
            print(f"\n⏳ [{i}/{len(STOCKS)}] Processing {symbol}...")
            df = get_cached_df(symbol)

            if df.empty or len(df) < 50:
                print(f"⚠️ Skipping {symbol}, not enough data")
                continue

            compute_all_indicators(df, cursor, symbol)

        conn.commit()
        conn.close()
        print("\n✅ All indicators processed successfully.")

    except Exception as e:
        print(f"❌ Error during indicator processing: {e}")

if __name__ == "__main__":
    run_all_indicators()
