# fetch_from_yf.py

import yfinance as yf
import os
import pandas as pd

CACHE_DIR = "/mnt/yf_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def fetch_from_yf(symbol):
    try:
        print(f"📈 Downloading {symbol} from Yahoo Finance (8y fallback)...")
        df = yf.download(symbol + ".NS", period="8y", interval="1d", progress=False)
        if df is None or df.empty:
            print(f"❌ No data for {symbol}")
            return None

        df = df.reset_index()
        df.rename(columns={
            "Date": "Date", "Open": "Open", "High": "High",
            "Low": "Low", "Close": "Close", "Adj Close": "Adj Close", "Volume": "Volume"
        }, inplace=True)

        path = os.path.join(CACHE_DIR, f"{symbol}.csv")
        df.to_csv(path, index=False)
        print(f"✅ Saved: {path}")
        return df

    except Exception as e:
        print(f"🚨 Error fetching {symbol}: {e}")
        return None
