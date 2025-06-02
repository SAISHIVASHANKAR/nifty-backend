# run_indicators.py

import sqlite3
from indicators import compute_all_indicators
from utils import get_db_connection
from stocks import STOCKS
import pandas as pd

def run_all():
    conn = get_db_connection()
    cursor = conn.cursor()

    for idx, symbol in enumerate(STOCKS.keys(), 1):
        try:
            print(f"[{idx}/{len(STOCKS)}] Processing: {symbol}")
            query = "SELECT * FROM prices WHERE symbol = ? ORDER BY date"
            df = pd.read_sql_query(query, conn, params=(symbol,))

            if df.empty or len(df) < 100:
                print(f"⚠️Skipping {symbol}: Not enough data")
                continue

            compute_all_indicators(df, cursor, symbol)

        except Exception as e:
            print(f"❌Error processing {symbol}: {e}")

    conn.commit()
    conn.close()
    print("✅All signals saved to DB.")

if __name__ == "__main__":
    run_all()
