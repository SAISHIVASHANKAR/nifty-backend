# run_indicators.py

import sqlite3
from indicators import compute_all_indicators
from utils import get_cached_df
from stocks import STOCKS

def run():
    conn = sqlite3.connect("nifty_stocks.db")
    cursor = conn.cursor()
    total = len(STOCKS)

    for i, symbol in enumerate(STOCKS, start=1):
        print(f"[{i}/{total}] Processing: {symbol}")
        df = get_cached_df(symbol)
        if df is not None and not df.empty:
            compute_all_indicators(df, cursor, symbol)
        else:
            print(f"⚠️ Skipping {symbol}: No usable DB data")

    conn.commit()
    conn.close()
    print("✅ All signals saved to DB.")

if __name__ == "__main__":
    run()
