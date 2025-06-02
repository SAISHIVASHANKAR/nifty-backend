# run_indicators.py

import sqlite3
from stocks import STOCKS
from utils import get_cached_df
from indicators import compute_all_indicators

# Create a single DB connection and cursor to be reused
conn = sqlite3.connect("nifty_stocks.db")
cursor = conn.cursor()

for symbol in STOCKS:
    df = get_cached_df(symbol)
    if df is None or df.empty or len(df) < 50:
        print(f"Skipping {symbol} due to insufficient or missing data.")
        continue

    try:
        compute_all_indicators(df, symbol, cursor)
        print(f"✅ Indicators for {symbol} inserted.")
    except Exception as e:
        print(f"❌ Failed for {symbol}: {e}")

conn.commit()
conn.close()
