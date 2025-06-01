# fetch_from_yf.py (updated to dynamically load all stock symbols)
import yfinance as yf
import sqlite3
from datetime import datetime
from utils import insert_into_prices_table
from stocks import STOCKS  # Use this if pulling from dict, or fetch from DB for full automation

def fetch_yf(symbol: str, years: int = 8):
    try:
        period = f"{years}y"
        print(f"📦Fetching {symbol} for {period}")
        ticker = yf.Ticker(symbol + ".NS")
        df = ticker.history(period=period)
        if df.empty:
            print(f"⚠️ No data returned for {symbol} ({period})")
            return False

        df.reset_index(inplace=True)
        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        df['Symbol'] = symbol
        insert_into_prices_table(df)
        print(f"✅{symbol} inserted into DB")
        return True

    except Exception as e:
        print(f"❌Error fetching {symbol} for {period}: {e}")
        return False

def fetch_all_symbols():
    for idx, symbol in enumerate(STOCKS):
        success = False
        for y in range(8, 0, -1):
            if fetch_yf(symbol, years=y):
                success = True
                break
        if not success:
            print(f"❌Skipped {symbol}: No usable data")

if __name__ == "__main__":
    fetch_all_symbols()
