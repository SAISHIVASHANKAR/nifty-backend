# run_indicators.py

from indicators import compute_all_indicators
from utils import get_cached_df
from stocks import STOCKS

import sqlite3

print("📊 Running indicators and saving signals to indicator_signals.db")

conn = sqlite3.connect("indicator_signals.db")
cursor = conn.cursor()

total = len(STOCKS)
count = 0

for symbol in STOCKS:
    count += 1
    print(f"\n📈 [{count}/{total}] Processing: {symbol}")

    df = get_cached_df(symbol)
    if df is None or df.empty:
        print(f"⚠️ Skipping {symbol}: No usable DB data")
        continue

    try:
        compute_all_indicators(symbol, df, cursor)
        conn.commit()
        print(f"✅ {symbol} inserted.")
    except Exception as e:
        print(f"❌ Failed for {symbol}: {e}")

conn.close()
