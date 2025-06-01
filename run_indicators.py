from indicators import compute_all_indicators
from utils import load_price_data
from stocks import STOCKS
import sqlite3

# Connect to SQLite once
conn = sqlite3.connect("indicator_signals.db")
cursor = conn.cursor()

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

for symbol in STOCKS:
    try:
        print(f"📊 Processing: {symbol}")
        df = load_price_data(symbol)
        if df is not None:
            compute_all_indicators(symbol, df, cursor)
    except Exception as e:
        print(f"❌ Error processing {symbol}: {e}")

conn.commit()
conn.close()
