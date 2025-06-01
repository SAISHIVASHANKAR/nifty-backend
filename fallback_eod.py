# fallback_eod.py

import requests
import pandas as pd
from utils import insert_into_prices_table
from datetime import datetime

EOD_API_TOKEN = "683461c4e4da71.25040803"

def fetch_eodhistorical(symbol):
    print(f"📦 Trying EODHistorical for {symbol}")
    try:
        url = f"https://eodhistoricaldata.com/api/eod/{symbol}.NSE?api_token={EOD_API_TOKEN}&fmt=json&period=d"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"❌ HTTP error {response.status_code} for {symbol} from EOD")
            return False

        data = response.json()
        if not data:
            print(f"❌ Empty data received from EOD for {symbol}")
            return False

        df = pd.DataFrame(data)
        df["Date"] = pd.to_datetime(df["date"])
        df.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume"}, inplace=True)
        df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]
        df.dropna(inplace=True)

        insert_into_prices_table(df, symbol)
        return True

    except Exception as e:
        print(f"❌ EODHistorical error for {symbol}: {e}")
        return False
