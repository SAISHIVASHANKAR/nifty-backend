from stocks import STOCKS
from utils import get_cached_df
from indicators import compute_all_indicators
import sqlite3

conn = sqlite3.connect("indicator_signals.db")
cursor = conn.cursor()

print("📊Running indicators and saving signals to indicator_signals.db")

for symbol in STOCKS.keys():
    print(f"📈Processing: {symbol}")
    try:
        df = get_cached_df(symbol)
        compute_all_indicators(symbol, df, cursor)
        print(f"✅{symbol} inserted.")
    except Exception as e:
        print(f"❌Failed to insert signal for {symbol}: {e}")

conn.commit()
conn.close()
