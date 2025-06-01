# fallback_bse.py (SQLite-compatible version)
import requests
import pandas as pd
from utils import insert_into_prices_table
from stocks import STOCKS
import time
from datetime import datetime

def fetch_fallback_bse(symbol):
    try:
        url = f"https://www.bseindia.com/stock-share-price/stockreach_stockquote.aspx?scripcode={symbol}&flag=sp"  # Note: placeholder
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            print(f"❌ BSE request failed for {symbol}")
            return None

        tables = pd.read_html(response.text)
        if not tables:
            print(f"❌ No data found for {symbol} from BSE")
            return None

        df = tables[0]  # BSE often places historical data in the first table

        if 'Date' not in df.columns:
            print(f"❌ Missing 'Date' in BSE response for {symbol}")
            return None

        df = df.rename(columns={
            'Open': 'Open', 'High': 'High', 'Low': 'Low',
            'Close': 'Close', 'Volume': 'Volume', 'Date': 'Date'
        })
        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        insert_into_prices_table(df, symbol)
        print(f"✅ BSE fallback inserted for {symbol}")
        return df

    except Exception as e:
        print(f"❌ Exception in fallback_bse for {symbol}: {e}")
        return None

def fetch_all_fallback_bse():
    for i, symbol in enumerate(STOCKS.keys(), 1):
        print(f"[{i}/{len(STOCKS)}] [BSE Fallback] {symbol}")
        fetch_fallback_bse(symbol)
        time.sleep(1.5)

if __name__ == "__main__":
    fetch_all_fallback_bse()
