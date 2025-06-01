# fetch_from_yf.py — updated with 8y→1y fallback and SQLite insert
import yfinance as yf
import pandas as pd
from utils import insert_into_prices_table

def fetch_from_yf(symbol):
    for years in range(8, 0, -1):  # 8y to 1y
        try:
            print(f"📥 Fetching {symbol} from Yahoo Finance: {years}y range")
            df = yf.download(f"{symbol}.NS", period=f"{years}y", interval="1d", progress=False)

            if df is not None and not df.empty:
                df.reset_index(inplace=True)
                df.rename(columns={
                    'Date': 'Date',
                    'Open': 'Open',
                    'High': 'High',
                    'Low': 'Low',
                    'Close': 'Close',
                    'Volume': 'Volume'
                }, inplace=True)

                df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
                df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')

                insert_into_prices_table(df, symbol)
                return df
            else:
                print(f"⚠️ Empty data for {symbol} with {years}y range")

        except Exception as e:
            print(f"❌ Yahoo fetch failed for {symbol} ({years}y): {e}")

    return None
