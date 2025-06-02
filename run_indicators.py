# run_indicators.py

import sqlite3
from indicators import compute_all_indicators
from stocks import STOCKS
from utils import get_cached_df

def run_all():
    conn = sqlite3.connect("nifty_stocks.db")
    cursor = conn.cursor()

    print("🔍 Running indicator evaluations...")
    for symbol in STOCKS.keys():
        df = get_cached_df(symbol)
        if df.empty:
            print(f"⚠️ No data found for {symbol}")
            continue

        compute_all_indicators(symbol, df, cursor)

    conn.commit()
    conn.close()
    print("✅ All indicators updated.")

if __name__ == "__main__":
    run_all()
