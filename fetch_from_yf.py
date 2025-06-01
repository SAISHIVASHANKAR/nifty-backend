# fetch_from_yf.py
import yfinance as yf
import sqlite3
import pandas as pd
from datetime import datetime
from stocks import STOCKS

DB_PATH = "nifty_stocks.db"

def insert_into_prices(symbol, df):
    """Insert price data into SQLite 'prices' table"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Prepare rows to insert
    rows = [
        (
            symbol,
            row["Date"],
            row["Open"],
            row["High"],
            row["Low"],
            row["Close"],
            row["Volume"]
        )
        for _, row in df.iterrows()
    ]

    # Insert
    cursor.executemany(
        "INSERT INTO prices (Symbol, Date, Open, High, Low, Close, Volume) VALUES (?, ?, ?, ?, ?, ?, ?)",
        rows
    )

    conn.commit()
    conn.close()

def fetch_and_store_yf(symbol):
    for years in range(8, 0, -1):  # Try 8y to 1y fallback
        try:
            print(f"📦 Fetching {symbol} for {years}y")
            data = yf.download(f"{symbol}.NS", period=f"{years}y", interval="1d", progress=False)

            if data.empty:
                continue

            df = data.reset_index()
            df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]
            df.dropna(inplace=True)

            if df.empty:
                continue

            # Format Date as string for SQLite
            df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
            insert_into_prices(symbol, df)
            print(f"✅ {symbol} inserted: {len(df)} rows")
            return True

        except Exception as e:
            print(f"⚠️ Error fetching {symbol} for {years}y: {e}")
    return False

def main():
    total = len(STOCKS)
    for i, symbol in enumerate(STOCKS, 1):
        print(f"\n[{i}/{total}] Processing: {symbol}")
        success = fetch_and_store_yf(symbol)
        if not success:
            print(f"❌ Skipped {symbol}: No usable data")

if __name__ == "__main__":
    main()
