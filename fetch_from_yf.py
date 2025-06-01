import yfinance as yf
import sqlite3
import pandas as pd
from stocks import STOCKS
from datetime import datetime
import os

DB_PATH = "nifty_stocks.db"

def fetch_and_store(symbol, years=8):
    print(f"📦Fetching {symbol} for {years}y")
    try:
        df = yf.download(f"{symbol}.NS", period=f"{years}y", auto_adjust=True)

        if df.empty:
            print(f"⚠️No data for {symbol} ({years}y)")
            return False

        df.reset_index(inplace=True)
        df["Symbol"] = symbol
        df.columns = [col.name if hasattr(col, "name") else col for col in df.columns]
        df = df[["Date", "Open", "High", "Low", "Close", "Volume", "Symbol"]]

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS prices (
                    Symbol TEXT,
                    Date TEXT,
                    Open REAL,
                    High REAL,
                    Low REAL,
                    Close REAL,
                    Volume REAL
                )
                """
            )
            df.to_sql("prices", conn, if_exists="append", index=False)
        print(f"✅{symbol} fetched from Yahoo ({years}y)")
        return True

    except Exception as e:
        print(f"❌Error fetching {symbol} for {years}y: {e}")
        return False

def main():
    for i, symbol in enumerate(list(STOCKS.keys())[:3], 1):  # TEMPORARY: test on 3
        print(f"\n[{i}/3] Processing: {symbol}")
        success = False
        for y in range(8, 0, -1):
            if fetch_and_store(symbol, y):
                success = True
                break
        if not success:
            print(f"❌Skipped {symbol}: No usable data")

if __name__ == "__main__":
    main()
