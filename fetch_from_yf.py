# fetch_from_yf.py

import yfinance as yf
from datetime import datetime, timedelta
from utils import insert_into_prices_table
from stocks import STOCKS

def fetch_yf(symbol, years=8):
    end = datetime.now()
    start = end - timedelta(days=years * 365)
    try:
        df = yf.download(f"{symbol}.NS", start=start.strftime('%Y-%m-%d'), end=end.strftime('%Y-%m-%d'), progress=False)
        if not df.empty:
            df.reset_index(inplace=True)
            df['Symbol'] = symbol
            insert_into_prices_table(df, symbol)  # ✅ REQUIRED ARGUMENT
            print(f"✅ {symbol} fetched from Yahoo ({years}y)")
            return df
        else:
            print(f"⚠️ No data for {symbol} ({years}y)")
    except Exception as e:
        print(f"❌ Error fetching {symbol} for {years}y:", e)
    return None

def fetch_all_symbols():
    for i, symbol in enumerate(STOCKS.keys(), 1):
        print(f"[{i}/{len(STOCKS)}] Processing: {symbol}")
        for y in range(8, 0, -1):
            df = fetch_yf(symbol, years=y)
            if df is not None:
                break
        else:
            print(f"❌ Skipped {symbol}: No usable data")

if __name__ == "__main__":
    fetch_all_symbols()
