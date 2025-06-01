# fetch_from_yf.py

import yfinance as yf
from datetime import datetime, timedelta
from utils import insert_into_prices_table, symbol_has_data

def fetch_from_yf(symbol):
    if symbol_has_data(symbol):
        print(f"⏭️ Skipping {symbol}: already exists in DB.")
        return True

    for years in range(8, 0, -1):
        try:
            end = datetime.today()
            start = end - timedelta(days=365 * years)
            print(f"🔹 Trying {years} year(s) for {symbol}...")
            df = yf.download(f"{symbol}.NS", start=start, end=end)

            if df.empty:
                continue

            df.reset_index(inplace=True)
            success = insert_into_prices_table(df, symbol)
            if success:
                return True
        except Exception as e:
            print(f"Yahoo fetch failed for {symbol} ({years}y): {e}")
            continue

    print(f"❌ Failed to fetch from Yahoo: {symbol}")
    return False
