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

def insert_indicator_signal(cursor, symbol, trend, momentum, volume, volatility, support_resistance):
    try:
        cursor.execute("""
            INSERT INTO indicator_signals 
            (symbol, trend, momentum, volume, volatility, support_resistance)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (symbol, trend, momentum, volume, volatility, support_resistance))
    except Exception as e:
        print(f"Error inserting signals for {symbol}: {e}")

def symbol_has_data(symbol):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM prices WHERE symbol = ?", (symbol,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    except Exception as e:
        print(f"DB check failed for {symbol}: {e}")
        return False
# utils.py

def insert_indicator_signal(cursor, symbol, trend, momentum, volume, volatility, support_resistance):
    try:
        cursor.execute('''
            INSERT OR REPLACE INTO indicator_signals (
                symbol, trend, momentum, volume, volatility, support_resistance
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (symbol, trend, momentum, volume, volatility, support_resistance))
    except Exception as e:
        print(f"DB insert error for signal {symbol}: {e}")
