# run_indicators.py

import sqlite3
from indicators import compute_all_indicators
from utils import get_cached_df
from stocks import STOCKS

print("Running indicators and saving signals to indicator_signals.db")

# Connect to the output database
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

symbols = list(STOCKS.keys())  # ✅ Dynamically load all stocks

for symbol in symbols:
    print(f"🗂️ Processing: {symbol}")
    try:
        df = get_cached_df(symbol)
        signal_data = compute_all_indicators(df)
        cursor.execute("""
            INSERT OR REPLACE INTO signals (symbol, trend, momentum, volume, volatility, support_resistance)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            symbol,
            signal_data.get("trend", 0),
            signal_data.get("momentum", 0),
            signal_data.get("volume", 0),
            signal_data.get("volatility", 0),
            signal_data.get("support_resistance", 0)
        ))
        conn.commit()
        print(f"✅ Saved indicators for {symbol}")
    except Exception as e:
        print(f"❌ Failed computing indicators for {symbol}: {e}")
        print(f"⚠️ Skipped {symbol}: No data or failed indicator computation.")

conn.close()
