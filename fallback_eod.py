import pandas as pd
import sqlite3
from datetime import datetime, timedelta
from stocks import STOCKS

DB_PATH = "nifty_stocks.db"

def fetch_eodhistorical(symbol):
    print(f"📦Fetching {symbol} from EOD Historical (mock)")

    try:
        # Simulated 10-day fallback
        df = pd.DataFrame({
            "Date": pd.date_range(end=datetime.today(), periods=10),
            "Open": [300 + i for i in range(10)],
            "High": [305 + i for i in range(10)],
            "Low": [295 + i for i in range(10)],
            "Close": [300 + i for i in range(10)],
            "Volume": [60000 + 10*i for i in range(10)],
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
        print(f"✅{symbol} inserted into DB from EOD Historical fallback")
        return True

    except Exception as e:
        print(f"❌EOD Historical fetch failed for {symbol}: {e}")
        return False

def main():
    for i, symbol in enumerate(list(STOCKS.keys())[:3], 1):  # TEMP TEST for 3 stocks
        print(f"\n[{i}/3] Trying EOD Historical fallback for {symbol}")
        fetch_eodhistorical(symbol)

if __name__ == "__main__":
    main()
