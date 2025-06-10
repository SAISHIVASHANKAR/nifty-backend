# fetch_and_cache_all.py

from stocks import STOCKS
from fetch_from_yf import fetch_from_yf
from fallback_chartink import fetch_chartink
from fallback_bse import fetch_bse
from fallback_eod import fetch_eodhistorical

for symbol in STOCKS:
    print(f"\n🔍 Fetching: {symbol}")

    if fetch_from_yf(symbol):
        print(f"✅ {symbol} inserted from Yahoo Finance.")
        continue

    if fetch_chartink(symbol):
        print(f"✅ {symbol} inserted from Chartink.")
        continue

    if fetch_eodhistorical(symbol):
        print(f"✅ {symbol} inserted from EOD Historical.")
        continue

    if fetch_bse(symbol):
        print(f"✅ {symbol} inserted from BSE.")
        continue

    print(f"❌ All data sources failed for {symbol}")
