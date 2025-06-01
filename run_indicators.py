# run_indicators.py

from indicators import compute_all_indicators
from utils import get_cached_df
from stocks import STOCKS
import sqlite3

conn = sqlite3.connect("indicator_signals.db")
cursor = conn.cursor()

# Create table if not exists
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

print("Running indicators and saving signals to indicator_signals.db")

# ✅ Dynamically load all symbols
symbols = list(STOCKS.keys())

for symbol in symbols:
    print(f"📋 Processing: {symbol}")
    try:
        df = get_cached_df(symbol)
        result = compute_all_indicators(df)
        cursor.execute("""
            INSERT OR REPLACE INTO signals (symbol, trend, momentum, volume, volatility, support_resistance)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (symbol, result["trend"], result["momentum"], result["volume"], result["volatility"], result["support_resistance"]))
        print(f"✅ Saved signals for {symbol}")
    except Exception as e:
        print(f"❌ Failed computing indicators for {symbol}: {e}")
        print(f"⚠️ Skipped {symbol}: No data or failed indicator computation.")

conn.commit()
conn.close()
