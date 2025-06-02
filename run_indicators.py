# run_indicators.py

from indicators import compute_all_indicators
from utils import get_db_connection
from stocks import STOCKS
import pandas as pd

def save_signals_to_db(signal_dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS indicator_signals (
            symbol TEXT PRIMARY KEY,
            trend INTEGER,
            momentum INTEGER,
            volume INTEGER,
            volatility INTEGER,
            support_resistance INTEGER,
            total_score INTEGER
        )
    """)
    for symbol, signals in signal_dict.items():
        cursor.execute("""
            INSERT OR REPLACE INTO indicator_signals (symbol, trend, momentum, volume, volatility, support_resistance, total_score)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            symbol,
            signals['trend'],
            signals['momentum'],
            signals['volume'],
            signals['volatility'],
            signals['support_resistance'],
            signals['total_score']
        ))
    conn.commit()
    conn.close()

def main():
    signal_summary = {}
    for symbol in STOCKS:
        try:
            result = compute_all_indicators(symbol)
            if result:
                signal_summary[symbol] = result
                print(f"✅ Processed {symbol}")
            else:
                print(f"❌ Skipped {symbol}: No result")
        except Exception as e:
            print(f"❌ Error processing {symbol}: {e}")
    save_signals_to_db(signal_summary)
    print("✅ All signals saved to DB.")

if __name__ == "__main__":
    main()
