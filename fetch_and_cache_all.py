# fetch_and_cache_all.py

from stocks import STOCKS
from fetch_from_yf import fetch_from_yf

print("Fetching EOD data and caching to nifty_stocks.db and /mnt/yf_cache")

for symbol in STOCKS:
    try:
        print(f"📦 Fetching: {symbol}")
        fetch_from_yf(symbol)
    except Exception as e:
        print(f"❌ Failed: {symbol} => {e}")
