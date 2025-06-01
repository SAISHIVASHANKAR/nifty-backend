# run_indicators.py

from indicators import compute_all_indicators
from utils import get_cached_df
from stocks import STOCKS

import sqlite3

print("📊 Running indicators and saving signals to indicator_signals.db")

# Connect to SQLite DB
conn = sqlite3.connect("indicator_signals.db")
cursor = conn.cursor()

# Iterate over all stock symbols
for symbol in STOCKS:
    print(f"📈 Processing: {symbol}")

    # Get cleaned DataFrame from cache
    df = get_cached_df(symbol)
    if df is None or df.empty:
        print(f"⚠️ Skipping {symbol}: No usable data")
        continue

    # Try computing and inserting signals
    try:
        compute_all_indicators(symbol, df, cursor)
        conn.commit()
        print(f"✅ {symbol} inserted.\n")
    except Exception as e:
        print(f"❌Failed to insert signal for {symbol}: {e}\n")

# Close DB connection
conn.close()
