# utils.py

import sqlite3
import pandas as pd

def get_db_connection():
    return sqlite3.connect("nifty_stocks.db")

def insert_into_prices_table(df, symbol):
    try:
        conn = get_db_connection()
        df = df.copy()
        df["symbol"] = symbol

        # Normalize column names to lowercase
        df.columns = df.columns.str.lower()

        # Retain only required columns
        required_cols = ["date", "open", "high", "low", "close", "volume", "symbol"]
        df = df[[col for col in required_cols if col in df.columns]]

        # Insert into database
        df.to_sql("prices", conn, if_exists="append", index=False)
        conn.close()
        return True

    except Exception as e:
        print(f"DB insert error for {symbol}: {e}")
        return False

def get_cached_df(symbol):
    try:
        conn = get_db_connection()
        query = f"SELECT * FROM prices WHERE symbol = ? ORDER BY date"
        df = pd.read_sql_query(query, conn, params=(symbol,))
        conn.close()
        return df
    except Exception as e:
        print(f"Error loading from DB for {symbol}: {e}")
        return pd.DataFrame()
