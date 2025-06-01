# fetch_and_cache_all.py

import yfinance as yf
import sqlite3
import pandas as pd
from stocks import STOCKS
from datetime import datetime
import time

DB_PATH = "nifty_stocks.db"

def create_prices_table():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            Symbol TEXT,
            Date TEXT,
            Open REAL,
            High REAL,
            Low REAL,
            Close REAL,
            Volume REAL
        )
    ''')
    conn.commit()
    conn.close()

def insert_to_db(symbol, df):
    if df is None or df.empty:
        return
    conn = sqlite3.connect(DB_PATH)
    df["Symbol"] = symbol
    df.to_sql("prices", conn, if_exists="append", index=False)
    conn.close()

def fetch_from_yahoo(symbol, years):
    try:
        print(f"📦 Fetching {symbol} for {years}y")
        df = yf.download(f"{symbol}.NS", period=f"{years}y", interval="1d", progress=False)
        if df.empty:
            return None
        df = df.reset_index()
        df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]
        df.dropna(inplace=True)
        df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
        return df
    except Exception as e:
        print(f"⚠️ Error fetching {symbol} for {years}y: {e}")
        return None

def main():
    create_prices_table()
    total = len(STOCKS)
    for idx, symbol in enumerate(STOCKS, start=1):
        print(f"\n[{idx}/{total}] Processing: {symbol}")
        for y in range(8, 0, -1):
            df = fetch_from_yahoo(symbol, y)
            if df is not None and not df.empty:
                try:
                    insert_to_db(symbol, df)
                    print(f"✅ Inserted {symbol} ({len(df)} rows)")
                    break
                except Exception as e:
                    print(f"❌ Insert error for {symbol}: {e}")
            time.sleep(1)
        else:
            print(f"❌ Skipped {symbol}: No usable data")

if __name__ == "__main__":
    main()
