# fallback_chartink.py

import requests
import pandas as pd
from utils import insert_into_prices_table
from datetime import datetime, timedelta

def fetch_chartink(symbol):
    print(f"📦 Trying Chartink for {symbol}")

    try:
        url = f"https://chartink.com/stocks/{symbol}.html"
        response = requests.get(url)

        if response.status_code != 200 or "Historical Data" not in response.text:
            print(f"❌ Chartink HTML invalid or stock not found: {symbol}")
            return False

        # This is a placeholder. Chartink does not offer clean HTML tables for EOD in response.
        print(f"❌ Chartink scraping not implemented: {symbol}")
        return False

    except Exception as e:
        print(f"❌ Chartink fallback error for {symbol}: {e}")
        return False
