# fallback_chartink.py (SQLite-safe version)
import requests
import pandas as pd
from utils import insert_into_prices_table
from stocks import STOCKS
import time
from datetime import datetime

def fetch_fallback_chartink(symbol):
    try:
        url = f"https://chartink.com/stocks/{symbol.lower()}.html"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"❌ Chartink request failed for {symbol}")
            return None

        # Extract table using pandas (assumes chartink exposes table)
        tables = pd.read_html(response.text)
        if not tables:
            print(f"❌ No tables found for {symbol} on Chartink")
            return None

        df = tables[0]
        if 'Date' not in df.columns:
            print(f"❌ Table structure invalid for {symbol}")
            return None

        df = df.rename(columns={
            'Open': 'Open', 'High': 'High', 'Low': 'Low',
            'Close': 'Close', 'Volume': 'Volume', 'Date': 'Date'
        })
        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        insert_into_prices_table(df, symbol)
        print(f"✅ Chartink data inserted for {symbol}")
        return df

    except Exception as e:
        print(f"❌ Exception in Chartink fallback for {symbol}: {e}")
        return None

def fetch_all_fallback_chartink():
    for i, symbol in enumerate(STOCKS.keys(), 1):
        print(f"[{i}/{len(STOCKS)}] [Chartink Fallback] {symbol}")
        fetch_fallback_chartink(symbol)
        time.sleep(1.5)  # Politeness delay

if __name__ == "__main__":
    fetch_all_fallback_chartink()
