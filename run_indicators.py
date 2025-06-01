import os
import sqlite3
from utils import get_cached_df
from indicators import compute_all_indicators
from stocks import STOCKS

# Connect to or create the SQLite database
conn = sqlite3.connect("indicator_signals.db")
cursor = conn.cursor()

# Create table if it doesn't exist
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

print("\U0001F4DD Running indicators and saving signals to indicator_signals.db")

for symbol in STOCKS:
    print(f"\U0001F4C4 Processing: {symbol}")
    try:
        df = get_cached_df(symbol)
        if df is None:
            print(f"⚠️ Skipped {symbol}: No data available.")
            continue
        signal_counts = compute_all_indicators(df)
        cursor.execute("REPLACE INTO signals VALUES (?, ?, ?, ?, ?, ?)",
                       (symbol,
                        signal_counts['trend'],
                        signal_counts['momentum'],
                        signal_counts['volume'],
                        signal_counts['volatility'],
                        signal_counts['support_resistance']))
        print(f"✅ Saved signals for {symbol}")
    except Exception as e:
        print(f"❌ Failed computing indicators for {symbol}: {e}")
        print(f"⚠️ Skipped {symbol}: No data or failed indicator computation.")

conn.commit()
conn.close()
