# fetch_from_yf.py
import yfinance as yf
import pandas as pd
from utils import insert_into_prices_table

def fetch_yf(symbol: str, years: int = 8) -> bool:
    try:
        print(f"📦Fetching {symbol} from Yahoo Finance: {years}y range")
        df = yf.download(f"{symbol}.NS", period=f"{years}y", auto_adjust=True)

        if df is None or df.empty:
            print(f"⚠️ No data found on Yahoo Finance for {symbol} ({years}y)")
            return False

        df = df.reset_index()
        df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]
        df.insert(0, "Symbol", symbol)

        insert_into_prices_table(df, symbol)
        print(f"✅{symbol} fetched successfully from Yahoo Finance.")
        return True

    except Exception as e:
        print(f"❌Error fetching {symbol} from Yahoo Finance: {e}")
        return False
