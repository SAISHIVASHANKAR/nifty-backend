# fetch_from_yf.py

import yfinance as yf
import pandas as pd
from utils import insert_into_prices_table

def fetch_from_yf(symbol):
    try:
        print(f"📡 Trying Yahoo Finance for {symbol}")
        ticker = yf.Ticker(f"{symbol}.NS")

        for period in ["8y", "7y", "6y", "5y", "4y", "3y", "2y", "1y"]:
            df = ticker.history(period=period)
            if df is not None and not df.empty:
                df = df.reset_index()
                df.rename(columns={
                    "Date": "date", "Open": "open", "High": "high",
                    "Low": "low", "Close": "close", "Volume": "volume"
                }, inplace=True)

                required_cols = ["date", "open", "high", "low", "close", "volume"]
                if not all(col in df.columns for col in required_cols):
                    print(f"⚠️ Missing columns in Yahoo data for {symbol}")
                    continue

                df = df[required_cols]
                success = insert_into_prices_table(df, symbol)
                return success

        print(f"❌ No valid Yahoo Finance data for {symbol}")
        return False

    except Exception as e:
        print(f"💥 Yahoo fetch failed for {symbol}: {e}")
        return False
