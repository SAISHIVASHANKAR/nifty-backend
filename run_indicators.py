import sqlite3
from indicators import compute_all_indicators
from stocks import STOCKS
from utils import get_cached_df

# Connect to SQLite
conn = sqlite3.connect("indicator_signals.db")
cursor = conn.cursor()

# Ensure the table exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS signals (
    symbol TEXT,
    trend INTEGER,
    momentum INTEGER,
    volume INTEGER,
    volatility INTEGER,
    support_resistance INTEGER,
    count INTEGER
)
""")
conn.commit()

print("📊 Running indicators and saving signals to indicator_signals.db")

# Loop through all stocks
for symbol in STOCKS:
    print(f"📈 Processing: {symbol}")
    try:
        df = get_cached_df(symbol)
        if df is None or df.empty:
            print(f"⚠️ Skipping {symbol}: No usable data")
            continue

        signals = compute_all_indicators(df)
        if not signals:
            print(f"⚠️ Skipping {symbol}: No signals returned")
            continue

        score = sum(signals.values())

        cursor.execute("""
        INSERT INTO signals (symbol, trend, momentum, volume, volatility, support_resistance, count)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            symbol,
            signals.get("trend", 0),
            signals.get("momentum", 0),
            signals.get("volume", 0),
            signals.get("volatility", 0),
            signals.get("support_resistance", 0),
            score
        ))

        conn.commit()
        print(f"✅ {symbol} inserted: Total Score = {score}")

    except Exception as e:
        print(f"❌ Error processing {symbol}: {e}")

conn.close()
