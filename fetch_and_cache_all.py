# fetch_and_cache_all.py

import time
import sqlite3
import pandas as pd
from stocks import STOCKS
from fetch_from_yf import fetch_yf
from fallback_eod import fetch_from_eodhistorical
from fallback_chartink import fetch_chartink
from fallback_bse import fetch_bse

DB_PATH = "nifty_stocks.db"
EOD_API_TOKEN = "683461c4e4da71.25040803"

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
    df["Symbol"] = symbol
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("prices", conn, if_exists="append", index=False)
    conn.close()

def fetch_with_fallbacks(symbol):
    for y in range(8, 0, -1):
        df = fetch_yf(symbol, y)
        if df is not None and not df.empty:
            print(f"✅ {symbol} fetched from Yahoo ({y}y)")
            return df

    df = fetch_from_eodhistorical(symbol, EOD_API_TOKEN)
    if df is not None and not df.empty:
        print(f"✅ {symbol} fetched from EOD Historical")
        return df

    df = fetch_chartink(symbol)
    if df is not None and not df.empty:
        print(f"✅ {symbol} fetched from Chartink")
        return df

    df = fetch_bse(symbol)
    if df is not None and not df.empty:
        print(f"✅ {symbol} fetched from BSE")
        return df

    print(f"❌ {symbol} fetch failed from all sources")
    return None

def main():
    create_prices_table()
    total = len(STOCKS)
    for idx, symbol in enumerate(STOCKS.keys(), 1):
        print(f"\n[{idx}/{total}] Processing: {symbol}")
        df = fetch_with_fallbacks(symbol)
        if df is not None:
            try:
                insert_to_db(symbol, df)
                print(f"🟢 {symbol} inserted ({len(df)} rows)")
            except Exception as e:
                print(f"❌ DB insert error for {symbol}: {e}")
        time.sleep(1)

if __name__ == "__main__":
    main()
