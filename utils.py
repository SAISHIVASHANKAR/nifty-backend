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

        df = df.rename(columns={
            "Date": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume"
        })

        df = df[["date", "open", "high", "low", "close", "volume", "symbol"]]
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

def symbol_has_data(symbol):
    try:
        conn = get_db_connection()
        query = "SELECT 1 FROM prices WHERE symbol = ? LIMIT 1"
        cur = conn.cursor()
        cur.execute(query, (symbol,))
        result = cur.fetchone()
        conn.close()
        return result is not None
    except Exception as e:
        print(f"DB check failed for {symbol}: {e}")
        return False

def insert_indicator_signal(symbol, category, signal):
    try:
        conn = get_db_connection()
        conn.execute(
            "CREATE TABLE IF NOT EXISTS indicator_signals (symbol TEXT, category TEXT, signal INTEGER)"
        )
        conn.execute(
            "DELETE FROM indicator_signals WHERE symbol = ? AND category = ?",
            (symbol, category),
        )
        conn.execute(
            "INSERT INTO indicator_signals (symbol, category, signal) VALUES (?, ?, ?)",
            (symbol, category, signal),
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ DB insert error for {symbol}, {category}: {e}")
        return False
