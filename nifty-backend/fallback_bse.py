# fallback_bse.py

import pandas as pd
from utils import insert_into_prices_table

def fetch_bse(symbol):
    try:
        print(f"🧵Trying BSE fallback data for {symbol} (stub logic)")

        # Dummy data frame with expected schema
        data = {
            "date": pd.date_range(end=pd.Timestamp.today(), periods=5).strftime("%Y-%m-%d"),
            "open": [201, 203, 204, 206, 207],
            "high": [205, 208, 209, 211, 210],
            "low": [200, 202, 203, 204, 205],
            "close": [204, 207, 208, 210, 209],
            "volume": [2000, 2100, 2200, 2300, 2400],
        }
        df = pd.DataFrame(data)

        # Insert into DB
        success = insert_into_prices_table(df, symbol)
        return success

    except Exception as e:
        print(f"❌ BSE fallback failed for {symbol}: {e}")
        return False
