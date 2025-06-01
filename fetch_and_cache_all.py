# fetch_and_cache_all.py

from fetch_from_yf import fetch_yf
from fallback_eod import fetch_eodhistorical
from fallback_chartink import fetch_chartink
from fallback_bse import fetch_bse
from stocks import STOCKS
import time

def fetch_with_fallbacks(symbol):
    print(f"[📦] Fetching {symbol} from Yahoo Finance: 8y range")
    try:
        success = fetch_yf(symbol)
        if success:
            print(f"✅ {symbol} inserted into DB from Yahoo Finance.")
            return
    except Exception as e:
        print(f"❌ Yahoo failed for {symbol}: {e}")

    print(f"📉 Trying fallback: EOD Historical for {symbol}")
    try:
        success = fetch_eodhistorical(symbol)
        if success:
            print(f"✅ {symbol} inserted into DB from EOD Historical.")
            return
    except Exception as e:
        print(f"❌ EOD Historical failed for {symbol}: {e}")

    print(f"📉 Trying fallback: Chartink for {symbol}")
    try:
        success = fetch_chartink(symbol)
        if success:
            print(f"✅ {symbol} inserted into DB from Chartink.")
            return
    except Exception as e:
        print(f"❌ Chartink failed for {symbol}: {e}")

    print(f"📉 Trying fallback: BSE for {symbol}")
    try:
        success = fetch_bse(symbol)
        if success:
            print(f"✅ {symbol} inserted into DB from BSE.")
            return
    except Exception as e:
        print(f"❌ BSE failed for {symbol}: {e}")

    print(f"❌ Skipped {symbol}: No usable data")

def main():
    symbols = list(STOCKS.keys())
    for idx, symbol in enumerate(symbols):
        print(f"\n[{idx+1}/{len(symbols)}] Processing: {symbol}")
        fetch_with_fallbacks(symbol)
        time.sleep(1)  # respectful rate limiting

if __name__ == "__main__":
    main()
