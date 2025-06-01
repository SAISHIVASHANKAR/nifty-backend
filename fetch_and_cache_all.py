# fetch_and_cache_all.py

from stocks import STOCKS
from fetch_from_yf import fetch_from_yf
from fallback_eod import fetch_eodhistorical
from fallback_chartink import fetch_chartink
from fallback_bse import fetch_bse
from utils import symbol_has_data

def fetch_with_fallbacks(symbol):
    if symbol_has_data(symbol):
        print(f"⏭️ Skipping {symbol}: already present in DB.")
        return True

    # 1. Try Yahoo Finance
    success = fetch_from_yf(symbol)
    if success:
        print(f"✅ {symbol} inserted into DB from Yahoo Finance.")
        return True

    # 2. Try EODHistorical
    print(f"📦 Fallback to EOD Historical for {symbol}")
    success = fetch_eodhistorical(symbol)
    if success:
        print(f"✅ {symbol} inserted into DB from EOD Historical.")
        return True

    # 3. Try Chartink
    print(f"📦 Fallback to Chartink for {symbol}")
    success = fetch_chartink(symbol)
    if success:
        print(f"✅ {symbol} inserted into DB from Chartink.")
        return True

    # 4. Try BSE
    print(f"📦 Fallback to BSE for {symbol}")
    success = fetch_bse(symbol)
    if success:
        print(f"✅ {symbol} inserted into DB from BSE.")
        return True

    print(f"❌ Failed to fetch {symbol} from all sources.")
    return False

def main():
    success_count = 0
    failure_count = 0
    total = len(STOCKS)

    for i, symbol in enumerate(STOCKS, 1):
        print(f"[{i}/{total}] Processing: {symbol}")
        if fetch_with_fallbacks(symbol):
            success_count += 1
        else:
            failure_count += 1

    print("\nFetch and cache completed.")
    print(f"✅ Total Success: {success_count}")
    print(f"❌ Total Failed: {failure_count}")

if __name__ == "__main__":
    main()
