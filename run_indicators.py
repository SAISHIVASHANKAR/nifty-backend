import sqlite3
from indicators import compute_all_indicators
from utils import get_cached_df
from stocks import STOCKS

# Connect to the SQLite database
conn = sqlite3.connect("indicator_signals.db")
cursor = conn.cursor()

# Create the signals table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS signals (
    symbol TEXT PRIMARY KEY,
    trend TEXT,
    momentum TEXT,
    volume TEXT,
    volatility TEXT,
    support_resistance TEXT
)
""")

print("Running indicators and saving signals to indicator_signals.db")

# Iterate through all stocks and evaluate indicators
for symbol in STOCKS:
    try:
        print(f"📈 Processing: {symbol}")
        df = get_cached_df(symbol)
        if df is None or df.empty:
            print(f"⏭️ Skipping {symbol}: No data")
            continue

        indicators = compute_all_indicators(df)
        if not indicators:
            print(f"⏭️ Skipping {symbol}: No indicators computed")
            continue

        trend = indicators.get("trend", "N/A")
        momentum = indicators.get("momentum", "N/A")
        volume = indicators.get("volume", "N/A")
        volatility = indicators.get("volatility", "N/A")
        support_resistance = indicators.get("support_resistance", "N/A")

        cursor.execute("""
            INSERT OR REPLACE INTO signals (
                symbol, trend, momentum, volume, volatility, support_resistance
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (symbol, trend, momentum, volume, volatility, support_resistance))

        print(f"✅ Saved: {symbol}")

    except Exception as e:
        print(f"❌ Error processing {symbol}: {e}")

conn.commit()
conn.close()
