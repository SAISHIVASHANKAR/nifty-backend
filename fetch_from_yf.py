# fetch_from_yf.py

import yfinance as yf
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
from utils import insert_into_prices_table

def fetch_yf(symbol: str, years: int, cursor=None):
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=years * 365)

        data = yf.download(
            f"{symbol}.NS",
            start=start_date.strftime('%Y-%m-%d'),
            end=end_date.strftime('%Y-%m-%d'),
            interval="1d",
            progress=False
        )

        if data.empty:
            print(f"⚠️ No data returned from Yahoo for {symbol} ({years}y)")
            return False

        data.reset_index(inplace=True)

        records = []
        for _, row in data.iterrows():
            records.append((
                symbol,
                row['Date'].strftime('%Y-%m-%d'),
                float(row['Open']) if not pd.isna(row['Open']) else None,
                float(row['High']) if not pd.isna(row['High']) else None,
                float(row['Low']) if not pd.isna(row['Low']) else None,
                float(row['Close']) if not pd.isna(row['Close']) else None,
                float(row['Volume']) if not pd.isna(row['Volume']) else None
            ))

        insert_into_prices_table(records, cursor)
        print(f"✅ {symbol} fetched from Yahoo ({years}y)")
        return True

    except Exception as e:
        print(f"❌ Error fetching {symbol} for {years}y: {e}")
        return False
