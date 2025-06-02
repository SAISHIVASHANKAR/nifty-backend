# run_indicators.py

import sqlite3
from indicators import compute_all_indicators

def run_all():
    conn = sqlite3.connect("nifty_stocks.db")
    cursor = conn.cursor()

    # Create table if not exists
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
    conn.commit()

    # Load all symbols from DB
    result = cursor.execute("SELECT DISTINCT symbol FROM prices")
    symbols = [row[0] for row in result.fetchall()]

    success_count = 0
    fail_count = 0

    for i, symbol in enumerate(symbols):
        print(f"[{i+1}/{len(symbols)}] Processing: {symbol}")
        try:
            df = cursor.execute("SELECT * FROM prices WHERE symbol = ? ORDER BY date", (symbol,))
            columns = [desc[0] for desc in df.description]
            rows = df.fetchall()

            import pandas as pd
            df = pd.DataFrame(rows, columns=columns)

            if df.empty or 'date' not in df.columns:
                raise ValueError("'date' column missing or empty")

            success = compute_all_indicators(df, cursor, symbol)
            if success:
                success_count += 1
            else:
                fail_count += 1

        except Exception as e:
            print(f"❌ Error processing {symbol}: {e}")
            fail_count += 1

    conn.commit()
    conn.close()
    print("✅ All signals saved to DB.")
    print(f"☑️ Total Success: {success_count}")
    print(f"❌ Total Failed: {fail_count}")

if __name__ == "__main__":
    run_all()
