import sqlite3
import pandas as pd

# Get DataFrame from DB
def get_cached_df(symbol):
    conn = sqlite3.connect("nifty_stocks.db")
    query = f"SELECT Date, Close, High, Low, Open, Volume FROM prices WHERE Symbol = ?"
    df = pd.read_sql(query, conn, params=[symbol], parse_dates=["Date"])
    conn.close()
    return df

# Insert new prices into DB table
def insert_into_prices_table(df, symbol):
    if df is None or df.empty:
        print(f"⚠️ Empty DataFrame for {symbol}, skipping DB insert.")
        return
    try:
        conn = sqlite3.connect("nifty_stocks.db")
        df["Symbol"] = symbol
        df["Date"] = pd.to_datetime(df["Date"]).dt.strftime('%Y-%m-%d')
        df.to_sql("prices", conn, if_exists="append", index=False)
        conn.close()
        print(f"✅ {symbol} inserted into DB")
    except Exception as e:
        print(f"❌ DB insert error for {symbol}: {e}")
