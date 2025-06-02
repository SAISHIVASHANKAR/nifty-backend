# run_indicators.py

from indicators import compute_all_indicators
from utils import insert_into_prices_table, insert_indicator_signal, get_all_symbols(cursor)
import sqlite3
import pandas as pd

# ✅ Connect to the SQLite database
conn = sqlite3.connect("nifty_stocks.db")
cursor = conn.cursor()

# ✅ Fetch all stock symbols
symbols = get_all_symbols()

print(f"📊 Total stocks: {len(symbols)}")

# ✅ Process each stock
for i, symbol in enumerate(symbols, 1):
    print(f"⏳[{i}/{len(symbols)}] Processing {symbol}...")

    try:
        # ✅ Read stock data from DB
        df = pd.read_sql_query(
            f"SELECT * FROM prices WHERE symbol = ? ORDER BY date ASC", conn, params=(symbol,)
        )

        if df.empty or len(df) < 30:
            print(f"⚠️ Skipped {symbol} — insufficient data.")
            continue

        # ✅ Ensure date column is datetime
        df["date"] = pd.to_datetime(df["date"], errors='coerce')

        # ✅ Drop rows with invalid dates
        df = df.dropna(subset=["date"])

        # ✅ Recompute indicators
        compute_all_indicators(df, symbol, cursor)

    except Exception as e:
        print(f"❌ compute_all_indicators() failed for {symbol}: {e}")

# ✅ Commit and close connection
conn.commit()
conn.close()
print("✅ All indicators processed.")
