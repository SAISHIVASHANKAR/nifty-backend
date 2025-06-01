import pandas as pd
import sqlite3
from datetime import datetime, timedelta
from stocks import STOCKS

DB_PATH = "nifty_stocks.db"

def fetch_bse(symbol):
    print(f"📦Fetching {symbol} from BSE (mock)")

    try:
        # Mock BSE fallback data generator
        df = pd.DataFrame({
            "Date": pd.date_range(end=datetime.today(), periods=10),
            "Open": [200 + i for i in range(10)],
            "High": [205 + i for i in range(10)],
            "Low": [195 + i for i in range(10)],
            "Close": [200 + i for i in range(10)],
            "Volume": [50000 + 10*i for i in range(10)],
            "Symbol": [symbol]*10
        })

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS prices (
                    Symbol TEXT,
                    Date TEXT,
                    Open REAL,
                    High REAL,
                    Low REAL,
                    Close REAL,
                    Volume REAL
                )
                """
            )
            df.to_sql("prices", conn, if_exists="append", index=False)
        print(f"✅{symbol} inserted into DB from BSE fallback")
        return True

    except Exception as e:
        print(f"❌BSE fetch failed for {symbol}: {e}")
        return False

def main():
    for i, symbol in enumerate(list(STOCKS.keys())[:3], 1):  # TEMP TEST for 3 stocks
        print(f"\n[{i}/3] Trying BSE fallback for {symbol}")
        fetch_bse(symbol)

if __name__ == "__main__":
    main()
