# fallback_bse.py

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

def fetch_bse(symbol):
    try:
        url = f"https://www.bseindia.com/BSEDATA/grossTurnOverData.aspx?text={symbol}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        if "No data" in response.text or not response.ok:
            print(f"❌ No BSE data for {symbol}")
            return None

        # Simulated CSV download or parsing logic placeholder
        # Example data format (you can replace this with actual CSV or HTML parsing)
        # Here, we simulate a DataFrame for demonstration:
        df = pd.DataFrame([
            {"Date": "2024-01-01", "Open": 2700, "High": 2750, "Low": 2680, "Close": 2725, "Volume": 1500000}
        ])
        return df

    except Exception as e:
        print(f"⚠️ BSE error for {symbol}: {e}")
        return None

def main(symbol):
    create_prices_table()
    df = fetch_bse(symbol)
    if df is not None:
        insert_into_db(symbol, df)
        print(f"✅ BSE inserted {symbol}: {len(df)} rows")
    else:
        print(f"❌ BSE failed for {symbol}")

# Example usage:
# main("RELIANCE")
