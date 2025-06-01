import os
import sqlite3
from utils import get_cached_df
from indicators import compute_all_indicators
from stocks import STOCKS

# Connect to SQLite DB
conn = sqlite3.connect("indicator_signals.db")
cursor = conn.cursor()

# Create the table if it doesn't exist
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

print("📊 Running indicators and saving signal counts to indicator_signals.db")

for symbol in sorted(STOCKS.keys()):
    print(f"🗂️ Processing: {symbol}")
    try:
        df = get_cached_df(symbol)
        if df is None or df.empty:
            print(f"⚠️ Skipped {symbol}: No data available.")
            continue
        signal_counts = compute_all_indicators(symbol, df)
        cursor.execute("""
            INSERT OR REPLACE INTO signals
            (symbol, trend, momentum, volume, volatility, support_resistance)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            symbol,
            signal_counts["trend"],
            signal_counts["momentum"],
            signal_counts["volume"],
            signal_counts["volatility"],
            signal_counts["support_resistance"]
        ))
        conn.commit()
        print(f"✅ Saved signals for {symbol}")
    except Exception as e:
        print(f"❌ Error computing indicators for {symbol}: {e}")

conn.close()
