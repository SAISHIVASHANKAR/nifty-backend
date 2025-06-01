# fetch_and_cache_all.py

from stocks import STOCKS
from fetch_from_yf import fetch_yf
from utils import init_db, insert_into_prices_table
import time

def fetch_with_fallbacks(symbol):
    # Try primary source (Yahoo)
    df = fetch_yf(symbol)
    return df

def main():
    print("⏳ Initializing database...")
    init_db()

    for i, symbol in enumerate(STOCKS.keys(), 1):
        print(f"\n[{i}/{len(STOCKS)}] Processing: {symbol}")
        try:
            df = fetch_with_fallbacks(symbol)
            if df is not None and not df.empty:
                insert_into_prices_table(df, symbol)
                print(f"✅ {symbol} inserted into DB")
            else:
                print(f"❌ Skipped {symbol}: No usable data")
        except Exception as e:
            print(f"❌ Error processing {symbol}: {e}")
        time.sleep(1)

if __name__ == "__main__":
    main()
