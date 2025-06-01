# fetch_from_yf.py

import yfinance as yf
import pandas as pd
from utils import insert_into_prices_table

def fetch_from_yf(symbol: str) -> bool:
    try:
        print(f"Attempting Yahoo Finance fetch for {symbol}")

        for period in ["8y", "7y", "6y", "5y", "4y", "3y", "2y", "1y"]:
            print(f"Trying {symbol} for period: {period}")
            data = yf.download(f"{symbol}.NS", period=period, interval="1d")

            if data is not None and not data.empty:
                data.reset_index(inplace=True)
                data = data.rename(columns={
                    "Date": "Date",
                    "Open": "Open",
                    "High": "High",
                    "Low": "Low",
                    "Close": "Close",
                    "Volume": "Volume"
                })

                data = data[["Date", "Open", "High", "Low", "Close", "Volume"]].dropna()
                data["Date"] = pd.to_datetime(data["Date"]).dt.strftime("%Y-%m-%d")

                success = insert_into_prices_table(data, symbol)
                return success
            else:
                print(f"No data found for {symbol} with period {period}, trying fallback period...")

        print(f"Yahoo Finance fetch failed for {symbol} after all fallbacks")
        return False

    except Exception as e:
        print(f"Yahoo Finance exception for {symbol}: {e}")
        return False
