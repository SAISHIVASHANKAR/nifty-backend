# run_indicators.py

import sqlite3
import pandas as pd
from indicators import compute_all_indicators
from stocks import STOCKS

def run():
    conn = sqlite3.connect("nifty_stocks.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS indicator_signals (
            symbol TEXT PRIMARY KEY,
            trend INTEGER,
            momentum INTEGER,
            volume INTEGER,
            volatility INTEGER,
            support_resistance INTEGER
        )
    """)

    for idx, symbol in enumerate(STOCKS.keys(), 1):
        try:
            print(f"[{idx}/{len(STOCKS)}] Processing: {symbol}")
            df = pd.read_sql_query(
                "SELECT * FROM prices WHERE symbol = ? ORDER BY date",
                conn, params=(symbol,)
            )
            if df.empty:
                print(f"⚠️ Skipping {symbol}: No usable DB data")
                continue

            compute_all_indicators(df, cursor, symbol)

        except Exception as e:
            print(f"❌ Error processing {symbol}: {e}")

    conn.commit()
    conn.close()
    print("✅ All signals saved to DB.")

if __name__ == "__main__":
    run()
