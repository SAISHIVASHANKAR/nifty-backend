# utils.py

import pandas as pd
import sqlite3

def get_cached_df(symbol):
    try:
        conn = sqlite3.connect("nifty_stocks.db")
        query = f"SELECT * FROM price_data WHERE symbol = ? ORDER BY date ASC"
        df = pd.read_sql_query(query, conn, params=(symbol,))
        conn.close()

        # Ensure expected columns exist
        expected = {'date', 'open', 'high', 'low', 'close', 'volume'}
        if not expected.issubset(df.columns):
            print(f"⚠️ Missing columns in {symbol}")
            return None

        # Convert columns to proper types
        df['open'] = pd.to_numeric(df['open'], errors='coerce')
        df['high'] = pd.to_numeric(df['high'], errors='coerce')
        df['low'] = pd.to_numeric(df['low'], errors='coerce')
        df['close'] = pd.to_numeric(df['close'], errors='coerce')
        df['volume'] = pd.to_numeric(df['volume'], errors='coerce')
        df.dropna(inplace=True)

        return df
    except Exception as e:
        print(f"❌ Failed to load {symbol} from DB: {e}")
        return None
