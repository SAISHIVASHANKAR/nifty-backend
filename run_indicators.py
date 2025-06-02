# run_indicators.py
import utils
print(dir(utils))
import sqlite3
from utils import (
    get_all_symbols,
    get_cached_df,
    insert_into_indicator_signal,
    get_db_connection
)
from indicators import compute_all_indicators

def run_all():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        symbols = get_all_symbols(cursor)

        print(f"🟡 Found {len(symbols)} symbols in DB")

        for symbol in symbols:
            print(f"🟠 Evaluating {symbol} ...")
            df = get_cached_df(symbol)

            if df.empty or len(df) < 50:
                print(f"⚠️ Skipping {symbol} due to insufficient data.")
                continue

            try:
                trend, momentum, volume, volatility, support_resistance = compute_all_indicators(df)

                insert_into_indicator_signal(
                    cursor,
                    symbol,
                    trend,
                    momentum,
                    volume,
                    volatility,
                    support_resistance
                )

                print(f"✅ Saved signals for {symbol}")

            except Exception as e:
                print(f"❌ Failed for {symbol}: {e}")
                continue

        conn.commit()
        conn.close()
        print("✅ All signals committed to DB")

    except Exception as e:
        print(f"🔥 Unexpected error during run_all: {e}")

if __name__ == "__main__":
    run_all()
