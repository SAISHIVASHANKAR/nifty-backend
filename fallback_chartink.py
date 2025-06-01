# fallback_chartink.py

import requests
import pandas as pd
import sqlite3
from datetime import datetime
from bs4 import BeautifulSoup

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

def fetch_chartink(symbol):
    url = f"https://chartink.com/stocks/{symbol}.html"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", {"class": "table table-sm table-hover text-sm text-center"})

        if not table:
            print(f"❌ No data table found for {symbol}")
            return None

        rows = table.find_all("tr")
        data = []
        for row in rows[1:]:
            cols = [col.text.strip() for col in row.find_all("td")]
            if len(cols) < 6:
                continue
            try:
                date = datetime.strptime(cols[0], "%d-%b-%y").strftime("%Y-%m-%d")
                data.append([
                    date,
                    float(cols[1].replace(",", "")),
                    float(cols[2].replace(",", "")),
                    float(cols[3].replace(",", "")),
                    float(cols[4].replace(",", "")),
                    float(cols[5].replace(",", ""))
                ])
            except:
                continue

        df = pd.DataFrame(data, columns=["Date", "Open", "High", "Low", "Close", "Volume"])
        return df
    except Exception as e:
        print(f"⚠️ Chartink error for {symbol}: {e}")
        return None

def main(symbol):
    create_prices_table()
    df = fetch_chartink(symbol)
    if df is not None:
        insert_into_db(symbol, df)
        print(f"✅ Chartink inserted {symbol}: {len(df)} rows")
    else:
        print(f"❌ Chartink failed for {symbol}")

# Example usage:
# main("RELIANCE")
