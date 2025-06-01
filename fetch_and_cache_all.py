# fetch_and_cache_all.py
from stocks import STOCKS
from fetch_from_yf import fetch_yf
from fallback_eod import fetch_eodhistorical
from fallback_chartink import fetch_chartink
from fallback_bse import fetch_bse

def main():
    print("🚀 Starting full EOD fetch process...\n")

    for i, symbol in enumerate(STOCKS.keys(), 1):
        print(f"\n[{i}/{len(STOCKS)}] Fetching {symbol} from Yahoo Finance...")

        success = fetch_yf(symbol)
        if success:
            print(f"✅ {symbol} inserted into DB from Yahoo Finance.")
            continue

        print(f"⚠️ Yahoo failed. Trying fallback sources for {symbol}...")

        if fetch_eodhistorical(symbol):
            print(f"✅ {symbol} inserted from EOD Historical.")
            continue

        if fetch_chartink(symbol):
            print(f"✅ {symbol} inserted from Chartink.")
            continue

        if fetch_bse(symbol):
            print(f"✅ {symbol} inserted from BSE.")
            continue

        print(f"❌ Skipped {symbol}: No usable data from any source.")

if __name__ == "__main__":
    main()
