# fallback_eod.py

import requests
import pandas as pd
from datetime import datetime
from utils import insert_into_prices_table, symbol_has_data

def fetch_eodhistorical(symbol):
    if symbol_has_data(symbol):
        print(f"⏭️ Skipping {symbol}: already exists in DB.")
        return True

    try:
        url = f"https://eodhistoricaldata.com/api/eod/{symbol}.NSE?api_token=683461c4e4da71.25040803&fmt=json"
        response = requests.get(url)
        data = response.json()

        if not data or 'error' in data:
            print(f"No data returned from EOD for {symbol}")
            return False

        df = pd.DataFrame(data)
        df["Date"] = pd.to_datetime(df["date"])
        df.rename(columns={
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume"
        }, inplace=True)

        df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]
        success = insert_into_prices_table(df, symbol)
        return success

    except Exception as e:
        print(f"EOD fetch failed for {symbol}: {e}")
        return False
