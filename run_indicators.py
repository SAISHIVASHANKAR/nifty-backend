# run_indicators.py

from stocks import STOCKS
from utils import get_cached_df
from indicators import compute_all_indicators
import sqlite3

# Connect to SQLite database
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
        support_resistance INTEGER,
        count INTEGER
    )
""")

print("📊 Running technical indicators for all stocks...\n")

for symbol in STOCKS.keys():
    print(f"📈 Processing: {symbol}")
    try:
        df = get_cached_df(symbol)
        if df is None or df.empty:
            print(f"⚠️ Skipped {symbol}: No data or empty DataFrame")
            continue
        compute_all_indicators(symbol, df, cursor)
    except Exception as e:
        print(f"❌ Failed to process {symbol}: {e}")

conn.commit()
conn.close()
print("\n✅ Done. All available signals inserted into indicator_signals.db.")
