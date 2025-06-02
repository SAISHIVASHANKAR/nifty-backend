# fallback_eod.py

import pandas as pd
from utils import insert_into_prices_table

def fetch_eodhistorical(symbol):
    try:
        print(f"🧕Trying EOD Historical fallback data for {symbol} (stub logic)")

        # Example stub data with proper column names and 5 fake rows
        data = {
            "date": pd.date_range(end=pd.Timestamp.today(), periods=5).strftime("%Y-%m-%d"),
            "open": [101, 103, 104, 106, 107],
            "high": [105, 108, 109, 111, 110],
            "low": [100, 102, 103, 104, 105],
            "close": [104, 107, 108, 110, 109],
            "volume": [1000, 1100, 1200, 1300, 1400],
        }
        df = pd.DataFrame(data)

        # Insert into database
        success = insert_into_prices_table(df, symbol)
        return success

    except Exception as e:
        print(f"❌ EOD Historical fallback failed for {symbol}: {e}")
        return False
