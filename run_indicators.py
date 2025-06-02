# run_indicators.py

from stocks import STOCKS
from utils import get_cached_df, insert_indicator_signal, get_db_connection
from indicators import compute_all_indicators

conn, cursor = get_db_connection()

for symbol in STOCKS:
    df = get_cached_df(symbol)
    if df is None or df.empty or len(df) < 50:
        print(f"Skipping {symbol} due to insufficient or missing data.")
        continue

    try:
        compute_all_indicators(df, symbol, cursor)
        print(f"✅ Indicators for {symbol} inserted.")
    except Exception as e:
        print(f"❌ Failed for {symbol}: {e}")

conn.commit()
conn.close()
