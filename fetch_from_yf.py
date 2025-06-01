# fetch_from_yf.py
import yfinance as yf
import sqlite3
import pandas as pd
from stocks import STOCKS
from datetime import datetime
import time

DB_PATH = "nifty_stocks.db"

def insert_to_db(symbol, df):
    conn = sqlite3.connect(DB_PATH)
    df["Symbol"] = symbol
    df.to_sql("prices", conn, if_exists="append", index=False)
    conn.close()

def fetch_yf(symbol, years):
    try:
        print(f"📦Fetching {symbol} for {years}y")
        period = f"{years}y"
        df = yf.download(f"{symbol}.NS", period=period)
        if df.empty:
            return None
        df = df.reset_index()
        df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]
        return df
    except Exception as e:
        print(f"⚠️Error fetching {symbol} for {years}y: {e}")
        return None

def main():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS prices (
        Symbol TEXT,
        Date TEXT,
        Open REAL,
        High REAL,
        Low REAL,
        Close REAL,
        Volume REAL
    )''')
    conn.close()

    for idx, symbol in enumerate(STOCKS.keys()):
        print(f"[{idx+1}/{len(STOCKS)}] Processing: {symbol}")
        for y in range(8, 0, -1):
            df = fetch_yf(symbol, y)
            if df is not None and not df.empty:
                try:
                    insert_to_db(symbol, df)
                    print(f"✅Inserted {symbol} ({len(df)} rows)")
                except Exception as e:
                    print(f"❌Insert error for {symbol}: {e}")
                break
            time.sleep(1)
        else:
            print(f"❌Skipped {symbol}: No usable data")

if __name__ == "__main__":
    main()
