# fetch_and_cache_all.py

from stocks import STOCKS
from fetch_from_yf import fetch_from_yf
from fallback_eod import fetch_eodhistorical
from fallback_chartink import fetch_chartink
from fallback_bse import fetch_bse

print("\nStarting full fetch and cache process\n")

success_count = 0
failure_count = 0

def fetch_with_fallbacks(symbol):
    # Try Yahoo Finance first
    print(f"☕️Fetching {symbol} from Yahoo Finance: 8y range")
    success = fetch_from_yf(symbol)
    if success:
        print(f"✅{symbol} inserted into DB from Yahoo Finance.")
        return True

    # Try EOD Historical next
    print(f"☕️Fallback to EOD Historical for {symbol}")
    success = fetch_eodhistorical(symbol)
    if success:
        print(f"✅{symbol} inserted into DB from EOD Historical.")
        return True

    # Try Chartink next
    print(f"☕️Fallback to Chartink for {symbol}")
    success = fetch_chartink(symbol)
    if success:
        print(f"✅{symbol} inserted into DB from Chartink.")
        return True

    # Try BSE last
    print(f"☕️Fallback to BSE for {symbol}")
    success = fetch_bse(symbol)
    if success:
        print(f"✅{symbol} inserted into DB from BSE.")
        return True

    print(f"❌Failed to fetch {symbol} from all sources")
    return False


for i, symbol in enumerate(STOCKS):
    print(f"\n[{i+1}/{len(STOCKS)}] Processing: {symbol}")
    try:
        if fetch_with_fallbacks(symbol):
            success_count += 1
        else:
            failure_count += 1
    except Exception as e:
        print(f"Exception during processing {symbol}: {e}")
        failure_count += 1

print("\nFetch and cache completed.")
print(f"✅ Total Success: {success_count}")
print(f"❌ Total Failed: {failure_count}")
