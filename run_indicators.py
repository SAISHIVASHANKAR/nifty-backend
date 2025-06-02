# run_indicators.py

from indicators import compute_all_indicators
from utils import get_cached_df, get_db_connection

from stocks import STOCKS

print("📊 Running indicators and saving signals to DB...\n")

total = len(STOCKS)
success = 0
failure = 0

for i, symbol in enumerate(STOCKS, 1):
    print(f"[{i}/{total}] Processing: {symbol}")
    df = get_cached_df(symbol)

    if df.empty:
        print(f"⚠️ Skipping {symbol}: No usable DB data")
        failure += 1
        continue

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        compute_all_indicators(df, symbol, cursor)
        conn.commit()
        conn.close()
        success += 1
    except Exception as e:
        print(f"❌ Error processing {symbol}: {e}")
        failure += 1

print("✅ All signals saved to DB.")
print(f"✔️ Total Success: {success}")
print(f"❌ Total Failed: {failure}")
