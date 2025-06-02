# run_indicators.py

import sqlite3
import pandas as pd
from utils import get_db_connection, get_cached_df
from indicators import compute_all_indicators

def run_all_indicator_evaluations():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Fetch distinct symbols from DB
        cursor.execute("SELECT DISTINCT symbol FROM prices")
        rows = cursor.fetchall()
        symbols = [row[0] for row in rows]

        print(f"🟢 Running indicators for {len(symbols)} stocks...\n")

        for i, symbol in enumerate(symbols, 1):
            print(f"[{i}/{len(symbols)}] Processing: {symbol}")

            df = get_cached_df(symbol)

            if df.empty or len(df) < 50:
                print(f"⚠️ Skipping {symbol}: insufficient data ({len(df)} rows)")
                continue

            try:
                compute_all_indicators(df, symbol, cursor)
            except Exception as e:
                print(f"❌ compute_all_indicators() failed for {symbol}: {e}")
                continue

        conn.commit()
        print("✅ All indicator signals inserted successfully.\n")

    except Exception as e:
        print(f"💥 Unexpected error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    run_all_indicator_evaluations()
