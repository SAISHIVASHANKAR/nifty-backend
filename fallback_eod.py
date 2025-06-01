# fallback_eod.py

import requests
import pandas as pd
import sqlite3
from datetime import datetime
import io

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

def insert_into_db(symbol, df):
    if df.empty:
        return
    df["Symbol"] = symbol
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("prices", conn, if_exists="append", index=False)
    conn.close()

def fetch_from_eodhistorical(symbol, api_token):
    try:
        url = f"https://eodhistoricaldata.com/api/eod/{symbol}.NSE?api_token={api_token}&fmt=csv&period=Y"
        response = requests.get(url, timeout=10)

        if not response.ok or "Error" in response.text:
            print(f"❌ EOD API failed for {symbol}")
            return None

        df = pd.read_csv(io.StringIO(response.text))
        df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]
        df.dropna(inplace=True)
        df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
        return df
    except Exception as e:
        print(f"⚠️ EOD error for {symbol}: {e}")
        return None

def main(symbol, api_token):
    create_prices_table()
    df = fetch_from_eodhistorical(symbol, api_token)
    if df is not None:
        insert_into_db(symbol, df)
        print(f"✅ EOD inserted {symbol}: {len(df)} rows")
    else:
        print(f"❌ EOD failed for {symbol}")

# ✅ Test run
if __name__ == "__main__":
    main("RELIANCE", "683461c4e4da71.25040803")
