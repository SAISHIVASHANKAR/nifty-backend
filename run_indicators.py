import sqlite3
import pandas as pd
from indicators import compute_all_indicators
from utils import get_all_symbols

conn = sqlite3.connect("nifty_stocks.db")
cursor = conn.cursor()

symbols = get_all_symbols(cursor)

print(f"📊 Total stocks: {len(symbols)}")

for i, symbol in enumerate(symbols, 1):
    print(f"⏳[{i}/{len(symbols)}] Processing {symbol}...")
    try:
        df = pd.read_sql_query(f"SELECT * FROM prices WHERE Symbol = '{symbol}' ORDER BY Date ASC", conn)
        df.columns = [col.lower() for col in df.columns]
        df['date'] = pd.to_datetime(df['date'])
        compute_all_indicators(df, symbol)
    except Exception as e:
        print(f"❌ compute_all_indicators() failed for {symbol}: {e}")

conn.close()
