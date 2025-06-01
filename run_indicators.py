import sqlite3
from indicators import compute_all_indicators
from utils import load_price_data
from stocks import STOCKS

conn = sqlite3.connect("indicator_signals.db")
cursor = conn.cursor()

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

for symbol in STOCKS:
    try:
        print(f"📊 Processing: {symbol}")
        df = load_price_data(symbol)
        compute_all_indicators(symbol, df, cursor)
    except Exception as e:
        print(f"❌ Failed computing indicators for {symbol}: {e}")

conn.commit()
conn.close()
