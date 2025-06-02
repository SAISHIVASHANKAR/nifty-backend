import sqlite3
import pandas as pd

DB_PATH = "nifty_stocks.db"

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def insert_into_prices_table(df, symbol):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for index, row in df.iterrows():
        cursor.execute(
            """INSERT OR REPLACE INTO prices (symbol, date, open, high, low, close, volume)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (symbol, row['Date'], row['Open'], row['High'], row['Low'], row['Close'], row['Volume'])
        )
    conn.commit()
    conn.close()

def insert_into_indicator_signal(cursor, symbol, trend, momentum, volume, volatility, support_resistance):
    cursor.execute(
        """INSERT OR REPLACE INTO indicator_signals
           (symbol, trend, momentum, volume, volatility, support_resistance)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (symbol, trend, momentum, volume, volatility, support_resistance)
    )

def get_all_symbols(cursor):
    cursor.execute("SELECT DISTINCT symbol FROM prices")
    results = cursor.fetchall()
    return [row[0] for row in results]

def get_cached_df(symbol):
    try:
        conn = sqlite3.connect(DB_PATH)
        query = "SELECT date, open, high, low, close, volume FROM prices WHERE symbol = ? ORDER BY date"
        df = pd.read_sql_query(query, conn, params=(symbol,))
        conn.close()
        return df
    except Exception as e:
        print(f"❌ DB read error for {symbol}: {e}")
        return pd.DataFrame()
