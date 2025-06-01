# fallback_eod.py (with EODHistorical token and proper DB insert)
import requests
import pandas as pd
from utils import insert_into_prices_table
from stocks import STOCKS
from datetime import datetime
import time

API_TOKEN = "683461c4e4da71.25040803"

def fetch_fallback_eod(symbol):
    try:
        url = f"https://eodhistoricaldata.com/api/eod/{symbol}.NSE?api_token={API_TOKEN}&fmt=csv"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"❌ EOD fallback failed for {symbol}: Status {response.status_code}")
            return None

        from io import StringIO
        df = pd.read_csv(StringIO(response.text))

        if 'date' not in df.columns:
            print(f"❌ Invalid CSV structure for {symbol}")
            return None

        df.rename(columns={
            'date': 'Date',
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'volume': 'Volume'
        }, inplace=True)

        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        insert_into_prices_table(df, symbol)
        print(f"✅ {symbol} inserted from EOD API")
        return df

    except Exception as e:
        print(f"❌ Exception during fallback EOD for {symbol}: {e}")
        return None

def fetch_all_fallback_eod():
    for i, symbol in enumerate(STOCKS.keys(), 1):
        print(f"[{i}/{len(STOCKS)}] [Fallback EOD] Fetching: {symbol}")
        fetch_fallback_eod(symbol)
        time.sleep(1.2)  # Respect API rate limits

if __name__ == "__main__":
    fetch_all_fallback_eod()
