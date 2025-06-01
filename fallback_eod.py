# fallback_eod.py

import pandas as pd
import sqlite3
from datetime import datetime, timedelta
from stocks import STOCKS

DB_PATH = "nifty_stocks.db"

def fetch_from_eodhistorical(symbol, token=None):  # token param kept for compatibility
    print(f"📦Fetching {symbol} from EOD Historical (mock)")

    try:
        # Mock 10-day data for fallback simulation
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
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS prices (
                    Symbol TEXT,
                    Date TEXT,
                    Open REAL,
                    High REAL,
                    Low REAL,
                    Close REAL,
                    Volume REAL
                )
            ''')
            df.to_sql("prices", conn, if_exists="append", index=False)
        print(f"✅{symbol} inserted into DB from EOD Historical fallback")
        return df

    except Exception as e:
        print(f"❌EOD Historical fallback failed for {symbol}: {e}")
        return None

def main():
    for i, symbol in enumerate(list(STOCKS.keys())[:3], 1):  # TEMP TEST: First 3 symbols
        print(f"\n[{i}/3] Trying EOD fallback for {symbol}")
        fetch_from_eodhistorical(symbol, token="demo")

if __name__ == "__main__":
    main()
