import requests
import pandas as pd
import sqlite3
from datetime import datetime
from stocks import STOCKS

DB_PATH = "nifty_stocks.db"

def fetch_chartink(symbol):
    print(f"📦Fetching {symbol} from Chartink (mock)")

    try:
        # Simulated Chartink fallback logic (replace this with real scraper if available)
        df = pd.DataFrame({
            "Date": pd.date_range(end=datetime.today(), periods=30),
            "Open": [100 + i for i in range(30)],
            "High": [105 + i for i in range(30)],
            "Low": [95 + i for i in range(30)],
            "Close": [100 + i for i in range(30)],
            "Volume": [100000 + 10*i for i in range(30)],
            "Symbol": [symbol]*30
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
        print(f"✅{symbol} inserted into DB from Chartink fallback")
        return True

    except Exception as e:
        print(f"❌Chartink fetch failed for {symbol}: {e}")
        return False

def main():
    for i, symbol in enumerate(list(STOCKS.keys())[:3], 1):  # TEMP TEST on 3 stocks
        print(f"\n[{i}/3] Trying Chartink fallback for {symbol}")
        fetch_chartink(symbol)

if __name__ == "__main__":
    main()
