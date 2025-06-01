# fetch_and_cache_all.py — master fallback-integrated EOD fetcher
from fetch_from_yf import fetch_from_yf
from fallback_eod import fetch_fallback_eod
from fallback_chartink import fetch_fallback_chartink
from fallback_bse import fetch_fallback_bse
from stocks import STOCKS
from utils import insert_into_prices_table
import time

def fetch_and_cache_all():
    for i, symbol in enumerate(STOCKS.keys(), 1):
        print(f"\n[{i}/{len(STOCKS)}] Fetching {symbol} from Yahoo Finance...")
        df = fetch_from_yf(symbol)
        if df is not None:
            if insert_into_prices_table(df, symbol):
                print(f"✅ {symbol} inserted into DB from Yahoo Finance.")
                continue

        print(f"🔁 Yahoo failed for {symbol}, trying EOD Historical...")
        df = fetch_fallback_eod(symbol)
        if df is not None and insert_into_prices_table(df, symbol):
            print(f"✅ {symbol} inserted into DB from EOD Historical.")
            continue

        print(f"🔁 EOD failed, trying Chartink for {symbol}...")
        df = fetch_fallback_chartink(symbol)
        if df is not None and insert_into_prices_table(df, symbol):
            print(f"✅ {symbol} inserted into DB from Chartink.")
            continue

        print(f"🔁 Chartink failed, trying BSE for {symbol}...")
        df = fetch_fallback_bse(symbol)
        if df is not None and insert_into_prices_table(df, symbol):
            print(f"✅ {symbol} inserted into DB from BSE.")
            continue

        print(f"❌ All sources failed for {symbol} — skipping.")
        time.sleep(1.2)

if __name__ == "__main__":
    fetch_and_cache_all()
